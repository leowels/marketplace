import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ChatAction
from pdf_handler import send_protected_pdf, create_sample_pdf
from config import BotConfig, Messages

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, BotConfig.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - main presentation message"""
    
    keyboard = [
        [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
        [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='leo_system')],
        [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
        [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
        [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(Messages.START_MESSAGE, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'get_pdf':
        await handle_pdf_request(query, context)
    elif query.data == 'leo_system':
        await handle_leo_system(query, context)
    elif query.data == 'want_bot':
        await handle_want_bot(query, context)
    elif query.data == 'mentorship':
        await handle_mentorship(query, context)
    elif query.data == 'download_pdf':
        await send_protected_pdf(query, context)
    elif query.data == 'back_to_main':
        await back_to_main(query, context)

async def handle_pdf_request(query, context) -> None:
    """Handle PDF guide request"""
    
    # Show typing action
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)

    keyboard = [
        [InlineKeyboardButton("📥 Скачать PDF", callback_data='download_pdf')],
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(Messages.PDF_INTRO, reply_markup=reply_markup)

async def handle_leo_system(query, context) -> None:
    """Handle Leo System explanation"""

    keyboard = [
        [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
        [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
        [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')],
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(Messages.LEO_SYSTEM_INFO, reply_markup=reply_markup)

async def handle_want_bot(query, context) -> None:
    """Handle bot request"""

    keyboard = [
        [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')],
        [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='leo_system')],
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(Messages.BOT_SERVICE, reply_markup=reply_markup)

async def handle_mentorship(query, context) -> None:
    """Handle mentorship request"""

    keyboard = [
        [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')],
        [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
        [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(Messages.MENTORSHIP, reply_markup=reply_markup)

async def back_to_main(query, context) -> None:
    """Return to main menu"""
    
    keyboard = [
        [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
        [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='leo_system')],
        [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
        [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
        [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(Messages.START_MESSAGE, reply_markup=reply_markup)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Validate configuration
    BotConfig.validate()
    
    # Create sample assets if they don't exist
    create_sample_pdf()
    
    # Create the Application
    application = Application.builder().token(BotConfig.BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    logger.info("Bot starting...")
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()