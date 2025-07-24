import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Константы
ADMIN_USERNAME = "leowels"
PDF_FILE_PATH = "leo_system_guide.pdf"

class LeoWelsBot:
    def __init__(self):
        self.application = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Стартовое сообщение с главным меню"""
        start_text = """Привет, это Leo.

Я не мотивирую. Я показываю путь.
Здесь ты получишь PDF-гайд, доступ к системе и можешь стартовать путь к 300к+ через Telegram.

👇 Выбери, с чего начнём:"""
        
        keyboard = [
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='about_system')],
            [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
            [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{ADMIN_USERNAME}')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(start_text, reply_markup=reply_markup)
        else:
            await update.callback_query.edit_message_text(start_text, reply_markup=reply_markup)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик всех callback кнопок"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'get_pdf':
            await self.send_pdf(query)
        elif query.data == 'about_system':
            await self.about_system(query)
        elif query.data == 'want_bot':
            await self.want_bot(query)
        elif query.data == 'mentorship':
            await self.mentorship(query)
        elif query.data == 'back_to_menu':
            await self.start(update, context)
    
    async def send_pdf(self, query) -> None:
        """Блок выдачи PDF-гайда"""
        pdf_text = """LEO SYSTEM: путь от 0 до 300к+

Забери гайд. Но помни: прочитать — мало.  
Реализация = деньги.

👇 Ниже кнопка:"""
        
        keyboard = [
            [InlineKeyboardButton("📥 Скачать PDF", callback_data='download_pdf')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(pdf_text, reply_markup=reply_markup)
    
    async def download_pdf(self, query) -> None:
        """Отправка PDF файла с защитой от пересылки"""
        user_id = query.from_user.id
        
        try:
            # Проверяем существование файла
            if os.path.exists(PDF_FILE_PATH):
                # Отправляем документ с защитой от пересылки
                with open(PDF_FILE_PATH, 'rb') as pdf_file:
                    await query.message.reply_document(
                        document=pdf_file,
                        filename="Leo_System_Guide.pdf",
                        caption="🔥 LEO SYSTEM GUIDE\n\nТеперь — реализуй!",
                        protect_content=True  # Защита от пересылки
                    )
            else:
                await query.message.reply_text(
                    "📁 PDF временно недоступен. Напишите @leowels для получения гайда."
                )
                
        except Exception as e:
            logger.error(f"Ошибка при отправке PDF: {e}")
            await query.message.reply_text(
                "⚠️ Произошла ошибка. Напишите @leowels для получения гайда."
            )
        
        # Возвращаем в меню
        keyboard = [[InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Что дальше?", reply_markup=reply_markup)
    
    async def about_system(self, query) -> None:
        """Информация о Leo System"""
        system_text = """Leo System — это система, которая помогает выстроить:
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
        
        keyboard = [
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
            [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(system_text, reply_markup=reply_markup)
    
    async def want_bot(self, query) -> None:
        """Информация о создании ботов"""
        bot_text = """Я собираю Telegram-ботов, которые:
– Продают
– Отбирают клиентов
– Работают 24/7

💰 Цена от 5 000 ₽
Всё под ключ. Без лишнего.

✍️ Хочешь — напиши: @leowels"""
        
        keyboard = [
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{ADMIN_USERNAME}')],
            [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='about_system')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(bot_text, reply_markup=reply_markup)
    
    async def mentorship(self, query) -> None:
        """Информация о наставничестве"""
        mentorship_text = """Я беру за руку и веду тебя к первым 100–300к.

– Без вложений
– Без реклам
– Только Telegram и система

💥 Старт — по заявке. Кол-во мест ограничено.

✍️ Напиши, если хочешь: @leowels"""
        
        keyboard = [
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{ADMIN_USERNAME}')],
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(mentorship_text, reply_markup=reply_markup)
    
    async def handle_download_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик загрузки PDF"""
        query = update.callback_query
        if query and query.data == 'download_pdf':
            await query.answer()
            await self.download_pdf(query)
    
    def run(self, token: str):
        """Запуск бота"""
        self.application = Application.builder().token(token).build()
        
        # Добавляем обработчики
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback, pattern='^(get_pdf|about_system|want_bot|mentorship|back_to_menu)$'))
        self.application.add_handler(CallbackQueryHandler(self.handle_download_pdf, pattern='^download_pdf$'))
        
        # Запускаем бота
        print("🤖 LeoWels Bot запущен!")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Главная функция"""
    # Получаем токен из переменных окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ Ошибка: Не найден TELEGRAM_BOT_TOKEN в переменных окружения")
        print("Установите токен: export TELEGRAM_BOT_TOKEN='your_bot_token'")
        return
    
    # Создаем и запускаем бота
    bot = LeoWelsBot()
    bot.run(token)

if __name__ == '__main__':
    main()