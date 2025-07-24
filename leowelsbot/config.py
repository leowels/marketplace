import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BotConfig:
    """Bot configuration class"""
    
    # Telegram Bot Token (required)
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    
    # Leo's username
    LEO_USERNAME = os.getenv('LEO_USERNAME', '@leowels')
    
    # Admin settings
    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID')
    
    # File paths
    ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
    PDF_PATH = os.path.join(ASSETS_DIR, 'leo_system_guide.pdf')
    
    # Bot settings
    PROTECT_CONTENT = True  # Prevent forwarding of sensitive content
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if BotConfig.BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            raise ValueError("Please set BOT_TOKEN in environment variables or .env file")
        
        return True

# Bot messages
class Messages:
    """Bot message templates"""
    
    START_MESSAGE = """Привет, это Leo.

Я не мотивирую. Я показываю путь.
Здесь ты получишь PDF-гайд, доступ к системе и можешь стартовать путь к 300к+ через Telegram.

👇 Выбери, с чего начнём:"""

    PDF_INTRO = """LEO SYSTEM: путь от 0 до 300к+

Забери гайд. Но помни: прочитать — мало.  
Реализация = деньги.

👇 Ниже кнопка:"""

    LEO_SYSTEM_INFO = """Leo System — это система, которая помогает выстроить:
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

    BOT_SERVICE = """Я собираю Telegram-ботов, которые:
– Продают
– Отбирают клиентов
– Работают 24/7

Цена от 5 000 ₽
Всё под ключ. Без лишнего.

✍️ Хочешь — напиши: @leowels"""

    MENTORSHIP = """Я беру за руку и веду тебя к первым 100–300к.

– Без вложений
– Без реклам
– Только Telegram и система

💥 Старт — по заявке. Кол-во мест ограничено.

✍️ Напиши, если хочешь: @leowels"""

    PDF_SUCCESS = "✅ PDF отправлен!\n\nИзучай систему и начинай применять."
    
    PDF_ERROR = "❌ Ошибка при отправке PDF.\n📲 Напишите @leowels для получения гайда."
    
    PDF_UNAVAILABLE = "📋 PDF временно недоступен. Напишите @leowels для получения гайда."