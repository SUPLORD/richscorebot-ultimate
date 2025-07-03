import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)

from handlers.start import start_handler
from handlers.goal import goal_handler
from handlers.report import report_handler
from handlers.callbacks import callback_query_handler
from jobs.reminders import schedule_reminders
from models.db import init_db

def main():
    # получаем токен и убираем невидимые символы
    TOKEN = os.getenv("BOT_TOKEN", "").strip()
    # выводим в лог для проверки
    print(f"DEBUG: BOT_TOKEN=[{TOKEN}] length={len(TOKEN)}")
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN пуст или не задан после strip()")
    # инициализация БД и планировщика
    init_db()
    schedule_reminders()
    # строим и запускаем приложение
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(goal_handler)
    app.add_handler(report_handler)
    app.add_handler(callback_query_handler)
    print("🚀 RICHSCORE 2.0 запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
