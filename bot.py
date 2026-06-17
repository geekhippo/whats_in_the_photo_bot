"""
What's in the Photo Bot — Telegram бот для описания изображений
Использует Google Gemini 1.5 Flash для анализа фотографий
"""

import os
import logging
import io
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import google.generativeai as genai

# ─── Настройки ───
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ─── Логирование ───
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── Gemini ───
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ─── Статистика ───
STATS_FILE = "/app/data/stats.json"


def _load_stats():
    import json
    try:
        os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"total_requests": 0, "users": {}}


def _save_stats(stats):
    import json
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def _record_usage(user_id, username=None):
    import time
    stats = _load_stats()
    stats["total_requests"] = stats.get("total_requests", 0) + 1
    uid = str(user_id)
    if uid not in stats.get("users", {}):
        stats["users"][uid] = {"count": 0, "username": username or "unknown"}
    stats["users"][uid]["count"] = stats["users"][uid].get("count", 0) + 1
    stats["users"][uid]["username"] = username or stats["users"][uid].get("username", "unknown")
    stats["users"][uid]["last_used"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _save_stats(stats)


# ─── Команды ───
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот-анализатор изображений.\n\n"
        "📸 Отправь мне фото или картинку, и я опишу что на ней изображено.\n\n"
        "🔧 Команды:\n"
        "/help — справка\n"
        "/stats — статистика"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Как пользоваться:\n\n"
        "1️⃣ Отправьте фото или картинку\n"
        "2️⃣ Я проанализирую изображение через Gemini AI\n"
        "3️⃣ Получите подробное описание на русском языке\n\n"
        "⚠️ Лимиты:\n"
        "- Максимальный размер фото: 20 МБ\n"
        "- Поддерживаемые форматы: JPG, PNG, WEBP, GIF\n\n"
        "🤖 Модель: Google Gemini 1.5 Flash"
    )


async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = _load_stats()
    total = stats.get("total_requests", 0)
    users = stats.get("users", {})
    unique_users = len(users)

    sorted_users = sorted(users.values(), key=lambda u: u.get("count", 0), reverse=True)[:5]
    top_lines = []
    for i, u in enumerate(sorted_users, 1):
        name = u.get("username", "unknown")
        count = u.get("count", 0)
        top_lines.append(f"  {i}. @{name} — {count} раз")
    top_text = "\n".join(top_lines) if top_lines else "  пока нет данных"

    text = (
        f"📊 Статистика бота\n\n"
        f"👥 Уникальных пользователей: {unique_users}\n"
        f"📝 Всего запросов: {total}\n\n"
        f"🏆 Топ-5 активных:\n{top_text}"
    )
    await update.message.reply_text(text)


# ─── Обработка изображений ───
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    _record_usage(user.id, user.username or user.first_name)

    # Показываем что бот думает
    await msg.reply_text("🔍 Анализирую изображение...")

    try:
        # Получаем фото в максимальном качестве
        photo = msg.photo[-1] if msg.photo else None
        document = msg.document if msg.document and msg.document.mime_type and msg.document.mime_type.startswith("image/") else None

        if not photo and not document:
            await msg.reply_text("⚠️ Не удалось найти изображение. Попробуйте отправить фото ещё раз.")
            return

        # Скачиваем файл
        if photo:
            file = await context.bot.get_file(photo.file_id)
        else:
            # Проверяем размер (лимит Gemini ~20MB)
            if document.file_size and document.file_size > 20 * 1024 * 1024:
                await msg.reply_text("⚠️ Файл слишком большой (максимум 20 МБ).")
                return
            file = await context.bot.get_file(document.file_id)

        # Скачиваем в память
        image_bytes = await file.download_as_bytearray()

        # Открываем изображение
        image = Image.open(io.BytesIO(image_bytes))

        # Конвертируем в RGB если нужно (для PNG с прозрачностью)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background

        # Отправляем в Gemini
        response = model.generate_content([
            "Опиши подробно что на этом изображении. Ответь на русском языке. "
            "Если на изображении есть текст — также прочитай и переведи его. "
            "Будь максимально детальным.",
            image
        ])

        # Отправляем ответ
        description = response.text if response.text else "Не удалось получить описание."

        # Telegram лимит — 4096 символов
        if len(description) > 4096:
            # Разбиваем на части
            parts = []
            while len(description) > 4096:
                split_pos = description.rfind('. ', 0, 4096)
                if split_pos <= 0:
                    split_pos = 4096
                parts.append(description[:split_pos + 1])
                description = description[split_pos + 1:]
            if description.strip():
                parts.append(description)

            for i, part in enumerate(parts):
                prefix = f"📸 Описание ({i+1}/{len(parts)}):\n\n" if len(parts) > 1 else "📸 Описание:\n\n"
                await msg.reply_text(prefix + part.strip())
        else:
            await msg.reply_text("📸 Описание:\n\n" + description)

    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {e}")
        await msg.reply_text(f"❌ Ошибка при анализе изображения: {e}")


# ─── Обработка текстовых сообщений ───
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Отправьте мне фото или картинку для анализа.\n"
        "Используйте /help для справки."
    )


# ─── Запуск ───
if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN не задан!")
        exit(1)
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY не задан!")
        exit(1)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("What's in the Photo Bot запущен...")
    app.run_polling()
