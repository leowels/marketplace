import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from config import BotConfig, Messages

logger = logging.getLogger(__name__)

async def send_protected_pdf(query, context) -> None:
    """Send PDF with protection against forwarding"""
    
    try:
        # Show uploading action
        await context.bot.send_chat_action(
            chat_id=query.message.chat_id, 
            action=ChatAction.UPLOAD_DOCUMENT
        )
        
        # Check if PDF exists
        if not os.path.exists(BotConfig.PDF_PATH):
            await query.edit_message_text(
                Messages.PDF_UNAVAILABLE,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')],
                    [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
                ])
            )
            return
        
        # Send PDF with protection
        with open(BotConfig.PDF_PATH, 'rb') as pdf_file:
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=pdf_file,
                filename="LEO_SYSTEM_Guide.pdf",
                caption="🎯 LEO SYSTEM: путь от 0 до 300к+\n\n💡 Изучи и применяй. Результат зависит от тебя.",
                protect_content=BotConfig.PROTECT_CONTENT,  # Prevent forwarding
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Вернуться в меню", callback_data='back_to_main')],
                    [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')]
                ])
            )
            
        # Update original message
        await query.edit_message_text(
            Messages.PDF_SUCCESS,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Вернуться в меню", callback_data='back_to_main')],
                [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')]
            ])
        )
        
        # Log successful delivery
        user_info = query.from_user
        logger.info(f"PDF delivered to user: {user_info.id} (@{user_info.username})")
        
    except Exception as e:
        logger.error(f"Error sending PDF: {e}")
        await query.edit_message_text(
            Messages.PDF_ERROR,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{BotConfig.LEO_USERNAME.replace("@", "")}')],
                [InlineKeyboardButton("🔙 Назад", callback_data='back_to_main')]
            ])
        )

def create_sample_pdf():
    """Create a sample PDF if it doesn't exist"""
    os.makedirs(BotConfig.ASSETS_DIR, exist_ok=True)
    
    if not os.path.exists(BotConfig.PDF_PATH):
        # Create a simple text file as placeholder
        sample_content = """LEO SYSTEM: путь от 0 до 300к+

Это демонстрационный файл.
Замените его на реальный PDF-гайд.

Содержание системы:
- Стратегии заработка в Telegram
- Построение личного бренда
- Автоматизация процессов
- Масштабирование бизнеса

Для получения полного гайда:
@leowels
"""
        
        with open(BotConfig.PDF_PATH.replace('.pdf', '_demo.txt'), 'w', encoding='utf-8') as f:
            f.write(sample_content)