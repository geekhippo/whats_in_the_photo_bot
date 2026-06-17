# 📸 What's in the Photo Bot

Telegram-бот для анализа изображений с помощью Google Gemini AI.
Отправьте боту фото или картинку — и получите подробное описание на русском языке.

## ✨ Возможности

- 📸 **Анализ фото** — подробное описание что на изображении
- 🔤 **Распознавание текста** — читает и переводит текст на фото
- 🎨 **Понимание контекста** — Gemini 1.5 Flash анализирует сцену, объекты, цвета
- 📊 **Статистика** — команда /stats
- 🐳 **Docker** — простое развертывание

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
echo "GEMINI_API_KEY=ваш_ключ_gemini" >> .env

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

### Google Gemini API Key

1. Перейдите на [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Создайте бесплатный аккаунт Google
3. Создайте API-ключ
4. Вставьте ключ в файл `.env`

## 🎯 Как использовать

1. Добавьте бота в чат или начните личный диалог
2. Отправьте фото или картинку
3. Бот проанализирует изображение через Gemini AI
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
- [google-generativeai](https://github.com/google/generative-ai-python) — Google Gemini AI
- [Pillow](https://python-pillow.org/) — обработка изображений

## 🤖 Модель

Используется **Google Gemini 1.5 Flash** — быстрая и точная мультимодальная модель:
- Бесплатный тариф: 15 запросов/минуту
- Поддержка изображений до 20 МБ
- Отличное качество описания на русском языке

## 📄 Лицензия

MIT License — свободное использование и модификация.

---

Сделано с ❤️ для сообщества [GeekHippo](https://geekhippo.ru)
