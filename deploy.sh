#!/bin/bash

# Скрипт развертывания LeoWels Bot
# Использование: ./deploy.sh

echo "🤖 Развертывание LeoWels Bot..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3."
    exit 1
fi

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip3."
    exit 1
fi

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Проверка токена бота
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️  Переменная TELEGRAM_BOT_TOKEN не установлена."
    echo "Введите токен вашего бота:"
    read -s BOT_TOKEN
    export TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
    echo "✅ Токен установлен."
fi

# Проверка PDF файла
if [ ! -f "leo_system_guide.pdf" ]; then
    echo "⚠️  PDF файл 'leo_system_guide.pdf' не найден."
    echo "Поместите PDF файл в текущую директорию или укажите путь в переменной PDF_FILE_PATH"
    echo "Продолжить без PDF? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "❌ Развертывание прервано."
        exit 1
    fi
fi

# Создание systemd сервиса (опционально)
create_service() {
    echo "📋 Создание systemd сервиса..."
    
    SERVICE_FILE="/etc/systemd/system/leowelsbot.service"
    CURRENT_DIR=$(pwd)
    USER=$(whoami)
    
    sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=LeoWels Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment=TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ExecStart=/usr/bin/python3 $CURRENT_DIR/bot_enhanced.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable leowelsbot.service
    
    echo "✅ Systemd сервис создан: leowelsbot.service"
    echo "Запуск: sudo systemctl start leowelsbot"
    echo "Остановка: sudo systemctl stop leowelsbot"
    echo "Статус: sudo systemctl status leowelsbot"
}

# Предложение создать сервис
echo "Создать systemd сервис для автозапуска? (y/n)"
read -r create_service_response
if [[ "$create_service_response" =~ ^[Yy]$ ]]; then
    create_service
fi

# Создание скрипта запуска
echo "📝 Создание скрипта запуска..."
cat > start_bot.sh << 'EOF'
#!/bin/bash
export TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
export ADMIN_USERNAME="${ADMIN_USERNAME:-leowels}"
export PDF_FILE_PATH="${PDF_FILE_PATH:-leo_system_guide.pdf}"

echo "🚀 Запуск LeoWels Bot..."
python3 bot_enhanced.py
EOF

chmod +x start_bot.sh

echo "✅ Скрипт запуска создан: start_bot.sh"

# Проверка конфигурации
echo "🔍 Проверка конфигурации..."
python3 -c "
try:
    from config import load_config
    config = load_config()
    print('✅ Конфигурация корректна')
    print(f'👤 Админ: @{config.admin_username}')
    print(f'📁 PDF файл: {config.pdf_file_path}')
except Exception as e:
    print(f'❌ Ошибка конфигурации: {e}')
    exit(1)
"

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📋 Что дальше:"
echo "1. Запустите бота: ./start_bot.sh"
echo "2. Или используйте: python3 bot_enhanced.py"
echo "3. Для постоянной работы: sudo systemctl start leowelsbot (если создали сервис)"
echo ""
echo "📊 Мониторинг:"
echo "- Логи: tail -f /var/log/syslog | grep leowelsbot"
echo "- Статистика: отправьте /stats боту от имени админа"
echo ""
echo "🔧 Настройка:"
echo "- Редактируйте config.py для изменения текстов"
echo "- Добавьте leo_system_guide.pdf для выдачи PDF"
echo ""
echo "🤖 Бот готов к работе!"