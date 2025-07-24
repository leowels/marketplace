import logging
import os
import asyncio
from datetime import datetime
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import TelegramError

from config import load_config, BotConfig

class LeoWelsBotEnhanced:
    def __init__(self, config: BotConfig):
        self.config = config
        self.application = None
        self.user_stats = {}  # Статистика пользователей
        
        # Настройка логирования
        logging.basicConfig(
            format=config.log_format,
            level=getattr(logging, config.log_level)
        )
        self.logger = logging.getLogger(__name__)
    
    def track_user_action(self, user_id: int, action: str) -> None:
        """Отслеживание действий пользователей"""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                'first_visit': datetime.now(),
                'actions': []
            }
        
        self.user_stats[user_id]['actions'].append({
            'action': action,
            'timestamp': datetime.now()
        })
        
        self.logger.info(f"User {user_id} performed action: {action}")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Стартовое сообщение с главным меню"""
        user_id = update.effective_user.id
        self.track_user_action(user_id, 'start')
        
        keyboard = [
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='about_system')],
            [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
            [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{self.config.admin_username}')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            if update.message:
                await update.message.reply_text(
                    self.config.start_message, 
                    reply_markup=reply_markup
                )
            else:
                await update.callback_query.edit_message_text(
                    self.config.start_message, 
                    reply_markup=reply_markup
                )
        except TelegramError as e:
            self.logger.error(f"Error in start method: {e}")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик всех callback кнопок"""
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()
        
        action_map = {
            'get_pdf': self.send_pdf,
            'about_system': self.about_system,
            'want_bot': self.want_bot,
            'mentorship': self.mentorship,
            'back_to_menu': lambda q: self.start(update, context),
            'download_pdf': self.download_pdf
        }
        
        if query.data in action_map:
            self.track_user_action(user_id, query.data)
            try:
                if query.data == 'back_to_menu':
                    await action_map[query.data](query)
                else:
                    await action_map[query.data](query)
            except TelegramError as e:
                self.logger.error(f"Error handling callback {query.data}: {e}")
    
    async def send_pdf(self, query) -> None:
        """Блок выдачи PDF-гайда"""
        keyboard = [
            [InlineKeyboardButton("📥 Скачать PDF", callback_data='download_pdf')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(self.config.pdf_message, reply_markup=reply_markup)
    
    async def download_pdf(self, query) -> None:
        """Отправка PDF файла с защитой от пересылки"""
        user_id = query.from_user.id
        
        try:
            # Проверяем существование файла
            if os.path.exists(self.config.pdf_file_path):
                # Отправляем документ с защитой от пересылки
                with open(self.config.pdf_file_path, 'rb') as pdf_file:
                    await query.message.reply_document(
                        document=pdf_file,
                        filename="Leo_System_Guide.pdf",
                        caption="🔥 LEO SYSTEM GUIDE\n\nТеперь — реализуй!",
                        protect_content=self.config.protect_pdf
                    )
                    
                # Отправляем уведомление админу о скачивании
                await self.notify_admin_pdf_download(user_id, query.from_user)
                    
            else:
                await query.message.reply_text(
                    f"📁 PDF временно недоступен. Напишите @{self.config.admin_username} для получения гайда."
                )
                
        except Exception as e:
            self.logger.error(f"Ошибка при отправке PDF: {e}")
            await query.message.reply_text(
                f"⚠️ Произошла ошибка. Напишите @{self.config.admin_username} для получения гайда."
            )
        
        # Возвращаем в меню
        keyboard = [[InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Что дальше?", reply_markup=reply_markup)
    
    async def notify_admin_pdf_download(self, user_id: int, user) -> None:
        """Уведомление админа о скачивании PDF"""
        try:
            admin_message = f"""📊 НОВОЕ СКАЧИВАНИЕ PDF
            
👤 Пользователь: {user.first_name} {user.last_name or ''}
🆔 ID: {user_id}
🕐 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}
📱 Username: @{user.username or 'не указан'}"""
            
            # Здесь можно добавить отправку уведомления админу
            self.logger.info(f"PDF downloaded by user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error notifying admin: {e}")
    
    async def about_system(self, query) -> None:
        """Информация о Leo System"""
        keyboard = [
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("🤖 Хочу свой бот", callback_data='want_bot')],
            [InlineKeyboardButton("🦁 Наставничество", callback_data='mentorship')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(self.config.system_message, reply_markup=reply_markup)
    
    async def want_bot(self, query) -> None:
        """Информация о создании ботов"""
        keyboard = [
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{self.config.admin_username}')],
            [InlineKeyboardButton("🧩 Что такое Leo System?", callback_data='about_system')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(self.config.bot_service_message, reply_markup=reply_markup)
    
    async def mentorship(self, query) -> None:
        """Информация о наставничестве"""
        keyboard = [
            [InlineKeyboardButton("📲 Написать Leo", url=f'https://t.me/{self.config.admin_username}')],
            [InlineKeyboardButton("📘 Получить PDF-гайд", callback_data='get_pdf')],
            [InlineKeyboardButton("← Назад в меню", callback_data='back_to_menu')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(self.config.mentorship_message, reply_markup=reply_markup)
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Статистика бота (только для админа)"""
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        # Проверяем, является ли пользователь админом
        if username != self.config.admin_username:
            await update.message.reply_text("❌ У вас нет доступа к этой команде")
            return
        
        total_users = len(self.user_stats)
        
        # Подсчет действий
        action_counts = {}
        for user_data in self.user_stats.values():
            for action_data in user_data['actions']:
                action = action_data['action']
                action_counts[action] = action_counts.get(action, 0) + 1
        
        stats_message = f"""📊 СТАТИСТИКА БОТА @leowelsbot

👥 Всего пользователей: {total_users}

📈 Действия:
"""
        
        for action, count in action_counts.items():
            stats_message += f"• {action}: {count}\n"
        
        await update.message.reply_text(stats_message)
    
    def run(self):
        """Запуск бота"""
        self.application = Application.builder().token(self.config.bot_token).build()
        
        # Добавляем обработчики
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stats", self.stats))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Запускаем бота
        print(f"🤖 LeoWels Bot Enhanced запущен!")
        print(f"👤 Админ: @{self.config.admin_username}")
        print(f"📁 PDF файл: {self.config.pdf_file_path}")
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Главная функция"""
    try:
        config = load_config()
        bot = LeoWelsBotEnhanced(config)
        bot.run()
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}")
        print("Установите токен: export TELEGRAM_BOT_TOKEN='your_bot_token'")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == '__main__':
    main()