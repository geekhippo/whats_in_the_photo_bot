# 📸 What's in the Photo Bot

Telegram-бот для анализа изображений с помощью AI.

🤖 **Попробовать бота:** [@Whats_in_the_photo_bot](https://t.me/Whats_in_the_photo_bot)
Отправьте боту фото или картинку — и получите подробное описание на русском языке.

## ✨ Возможности

- 📸 **Анализ фото** — подробное описание что на изображении
- 🔤 **Распознавание текста** — читает и переводит текст на фото
- 🎨 **Понимание контекста** — AI анализирует сцену, объекты, цвета
- 📊 **Статистика** — команда /stats
- 🐳 **Docker** — простое развертывание
- 🔄 **Автоматическое разбиение** — длинные ответы разбиваются на части

## 🚀 Быстрый старт

### Одной командой

```bash
curl -fsSL https://raw.githubusercontent.com/geekhippo/whats_in_the_photo_bot/master/install.sh | bash
```

### Или вручную

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/geekhippo/whats_in_the_photo_bot.git
cd whats_in_the_photo_bot

# 2. Создайте .env с токенами
echo "TELEGRAM_TOKEN=ваш_токен" > .env
echo "OPENROUTER_API_KEY=ваш_ключ_openrouter" >> .env

# 3. Соберите и запустите
docker build -t whats-in-the-photo-bot .
docker run --name whats-in-the-photo-bot --env-file .env -d --restart unless-stopped whats-in-the-photo-bot
```

## 📝 Как получить ключи

### Telegram Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям — получите токен вида `123456:ABC-DEF1234gh...`
4. Вставьте токен в файл `.env`

### OpenRouter API Key

1. Перейдите на [openrouter.ai](https://openrouter.ai/keys)
2. Зарегистрируйтесь (бесплатно)
3. Создайте API-ключ
4. Вставьте ключ в файл `.env`

## 🎯 Как использовать

1. Добавьте бота в чат или начните личный диалог
2. Отправьте фото или картинку
3. Бот проанализирует изображение через AI
4. Получите подробное описание на русском языке

## 📁 Структура проекта

```
whats_in_the_photo_bot/
├── bot.py              # Основной код бота
├── Dockerfile          # Docker-образ
├── requirements.txt    # Python-зависимости
├── install.sh          # Скрипт установки
└── README.md           # Документация
```

## 🛠️ Команды управления

```bash
# Запуск
docker start whats-in-the-photo-bot

# Остановка
docker stop whats-in-the-photo-bot

# Логи
docker logs -f whats-in-the-photo-bot

# Перезапуск
docker restart whats-in-the-photo-bot

# Обновление
cd whats_in_the_photo_bot && git pull && docker build -t whats-in-the-photo-bot . && docker restart whats-in-the-photo-bot
```

## 📦 Зависимости

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) — работа с Telegram API
- [httpx](https://github.com/encode/httpx) — HTTP-клиент для OpenRouter API
- [Pillow](https://python-pillow.org/) — обработка изображений

## 🤖 Модель

Используется **nex-agi/nex-n2-pro:free** через OpenRouter:
- Бесплатный тариф
- Поддержка изображений
- Контекст: 262K токенов
- Качественное описание на русском языке

## 📄 Лицензия

MIT License — свободное использование и модификация.

---

Сделано с ❤️ для сообщества [GeekHippo](https://geekhippo.ru)
