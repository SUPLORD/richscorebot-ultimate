from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, MessageHandler, filters, ContextTypes, CommandHandler

GOAL, AMOUNT, MONTHLY, PERSONALITY = range(4)

async def goal_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["goal"] = update.message.text
    await update.message.reply_text("Сколько нужно (в рублях)?", reply_markup=ReplyKeyboardRemove())
    return AMOUNT

async def amount_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["amount"] = int(update.message.text.replace(" ",""))
    await update.message.reply_text("Сколько откладываешь в месяц?")
    return MONTHLY

async def monthly_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["monthly"] = int(update.message.text.replace(" ",""))
    keyboard = [[InlineKeyboardButton("📄 Отчёт", callback_data="report")]]
    await update.message.reply_text("Готово! Нажми кнопку, чтобы получить PDF:", reply_markup=InlineKeyboardMarkup(keyboard))
    return ConversationHandler.END

goal_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, goal_step)],
    states={
        AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_step)],
        MONTHLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, monthly_step)],
    },
    fallbacks=[CommandHandler("cancel", lambda u,c: ConversationHandler.END)]
)
