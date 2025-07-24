import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class BotConfig:
    """Конфигурация бота"""
    # Основные настройки
    bot_token: str
    admin_username: str = "leowels"
    pdf_file_path: str = "leo_system_guide.pdf"
    
    # Настройки логирования
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Защита контента
    protect_pdf: bool = True
    
    # Тексты сообщений
    start_message: str = """Привет, это Leo.

Я не мотивирую. Я показываю путь.
Здесь ты получишь PDF-гайд, доступ к системе и можешь стартовать путь к 300к+ через Telegram.

👇 Выбери, с чего начнём:"""

    pdf_message: str = """LEO SYSTEM: путь от 0 до 300к+

Забери гайд. Но помни: прочитать — мало.  
Реализация = деньги.

👇 Ниже кнопка:"""

    system_message: str = """Leo System — это система, которая помогает выстроить:
- Личность с влиянием
- Доход через Telegram
- Воронку, которая работает за тебя

📦 Внутри:
– PDF-гайды
– Боты
– Скрипты
– Наставничество
– Франшиза

👑 Ты не клиент. Ты становишься системой."""

    bot_service_message: str = """Я собираю Telegram-ботов, которые:
– Продают
– Отбирают клиентов
– Работают 24/7

💰 Цена от 5 000 ₽
Всё под ключ. Без лишнего.

✍️ Хочешь — напиши: @leowels"""

    mentorship_message: str = """Я беру за руку и веду тебя к первым 100–300к.

– Без вложений
– Без реклам
– Только Telegram и система

💥 Старт — по заявке. Кол-во мест ограничено.

✍️ Напиши, если хочешь: @leowels"""

def load_config() -> BotConfig:
    """Загружает конфигурацию из переменных окружения"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в переменных окружения")
    
    return BotConfig(
        bot_token=bot_token,
        admin_username=os.getenv('ADMIN_USERNAME', 'leowels'),
        pdf_file_path=os.getenv('PDF_FILE_PATH', 'leo_system_guide.pdf'),
        log_level=os.getenv('LOG_LEVEL', 'INFO'),
        protect_pdf=os.getenv('PROTECT_PDF', 'true').lower() == 'true'
    )