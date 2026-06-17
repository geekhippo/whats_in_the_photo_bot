#!/bin/bash

echo "🚀 Установка What's in the Photo Bot..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Docker не найден. Устанавливаю..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

# Создание директории
mkdir -p whats_in_the_photo_bot
cd whats_in_the_photo_bot

# Запрос данных
echo "📝 Нам понадобятся ключи для работы бота."
read -p "Введите TELEGRAM_TOKEN: " TELEGRAM_TOKEN < /dev/tty
echo "🔑 Нужен OpenRouter API Key."
echo "   Получить бесплатно: https://openrouter.ai/keys"
read -p "Введите OPENROUTER_API_KEY: " OPENROUTER_API_KEY < /dev/tty

cat <<EOF > .env
TELEGRAM_TOKEN=$TELEGRAM_TOKEN
OPENROUTER_API_KEY=$OPENROUTER_API_KEY
EOF

# Скачивание файлов
echo "📥 Скачиваю файлы бота..."
curl -sSL https://raw.githubusercontent.com/geekhippo/whats_in_the_photo_bot/master/bot.py -o bot.py
curl -sSL https://raw.githubusercontent.com/geekhippo/whats_in_the_photo_bot/master/Dockerfile -o Dockerfile
curl -sSL https://raw.githubusercontent.com/geekhippo/whats_in_the_photo_bot/master/requirements.txt -o requirements.txt

# Сборка и запуск
echo "🏗️ Собираю и запускаю бота..."
docker build -t whats-in-the-photo-bot .
docker stop whats-in-the-photo-bot 2>/dev/null || true
docker rm whats-in-the-photo-bot 2>/dev/null || true
docker run --name whats-in-the-photo-bot --env-file .env -d --restart unless-stopped whats-in-the-photo-bot

echo "🎉 Готово! What's in the Photo Bot запущен."
echo ""
echo "Возможности бота:"
echo "  📸 Анализ фото и картинок через AI"
echo "  📝 Подробное описание на русском языке"
echo "  🔤 Распознавание текста на изображениях"
echo "  📊 Команда /stats"
echo ""
echo "Логи: docker logs -f whats-in-the-photo-bot"
