import os
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.goal import goal_handler

def main():
    TOKEN = os.getenv("BOT_TOKEN", "").strip()
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN не задан!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(start_handler)
    app.add_handler(goal_handler)

    print("🚀 RICHSCORE PRO запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
