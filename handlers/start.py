from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CommandHandler, ContextTypes

NAME = 0

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я RICHSCORE 2.0 — твой финансовый PRO-ассистент.\nКак к тебе обращаться?"
    )
    return NAME

async def get_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["name"] = update.message.text
    keyboard = [["Квартира","Машина"],["Бизнес","Путешествие"],["✍️ Своя цель"]]
    await update.message.reply_text(
        f"Приятно познакомиться, {ctx.user_data['name']}!\nВыбери цель:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return ConversationHandler.END

start_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)]},
    fallbacks=[CommandHandler("cancel", lambda u,c: ConversationHandler.END)]
)
