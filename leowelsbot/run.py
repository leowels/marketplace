#!/usr/bin/env python3
"""
Leo System Presentation Bot Runner
Simple script to start the bot with proper error handling
"""

import sys
import logging
from bot import main

def run_bot():
    """Run the Leo System bot with error handling"""
    try:
        print("🤖 Запуск Leo System Presentation Bot...")
        print("📋 Проверка конфигурации...")
        
        # Start the bot
        main()
        
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        logging.error(f"Bot startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()