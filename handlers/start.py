from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.first_name
    await update.message.reply_text(
        f"👋 Привет, {user}! Я RICHSCORE PRO.\n"
        "Сейчас быстро разложим твои финансы по полочкам 📊. "
        "Жми /goal и погнали к мечте!"
    )

start_handler = CommandHandler("start", start)
