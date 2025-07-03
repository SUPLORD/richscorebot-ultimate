from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from utils.pdf import make_report

async def report_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    data = ctx.user_data
    pdf = make_report(data)
    await update.callback_query.message.reply_document(pdf)
    await update.callback_query.answer()

report_handler = CallbackQueryHandler(report_callback, pattern="^report$")
