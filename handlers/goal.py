from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler,
    filters, ContextTypes
)

GOAL, CUSTOM_GOAL, AMOUNT, RATE = range(4)

async def goal_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    buttons = [["🚗 Машина", "🏠 Квартира"], ["💼 Бизнес", "🌴 Путешествие"], ["📱 Айфон", "🎯 Свой вариант"]]
    await update.message.reply_text(
        "Выбери цель из списка или предложи свою:",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
    return GOAL

async def custom_goal_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data['goal'] = update.message.text
    await update.message.reply_text("Отличный выбор! Сколько ₽ потребуется?", reply_markup=ReplyKeyboardRemove())
    return AMOUNT

async def amount_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["goal"] = update.message.text
    if update.message.text == "🎯 Свой вариант":
        await update.message.reply_text("Напиши свою уникальную цель:", reply_markup=ReplyKeyboardRemove())
        return CUSTOM_GOAL
    await update.message.reply_text(f"Отлично! Какая сумма нужна для цели «{ctx.user_data['goal']}»?", reply_markup=ReplyKeyboardRemove())
    return AMOUNT

async def rate_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    amount_text = update.message.text.replace(" ", "")
    if amount_text.isdigit():
        ctx.user_data["amount"] = int(amount_text)
        await update.message.reply_text("Теперь напиши процентную ставку вклада, на которую рассчитываешь (например, 10.5):")
        return RATE
    else:
        await update.message.reply_text("Это не похоже на число, давай ещё раз:")
        return AMOUNT

async def final_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        rate = float(update.message.text.replace(",", "."))
        goal = ctx.user_data["goal"]
        amount = ctx.user_data["amount"]

        months_low = round(amount / 10000)
        months_medium = round(amount / 20000)
        months_high = round(amount / 50000)

        text = (
            f"🎯 Цель: {goal}\n"
            f"💰 Сумма: {amount:,} ₽\n"
            f"📈 Ставка вклада: {rate}%\n\n"
            "🔹 Стратегии достижения цели:\n"
            f"🐢 Медленно (низкий риск): ~{months_low} месяцев\n"
            f"🚶 Средний темп (умеренный риск): ~{months_medium} месяцев\n"
            f"🚀 Быстро (высокий риск): ~{months_high} месяцев\n\n"
            "⚠️ Это не финансовая рекомендация, а дружеский расчёт в соответствии с законами РФ."
        )

        await update.message.reply_text(text)
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Это не процент! Напиши ставку цифрами, например, 8.5:")
        return RATE

goal_handler = ConversationHandler(
    entry_points=[CommandHandler("goal", goal_step)],
    states={
        GOAL: [MessageHandler(filters.TEXT & (~filters.COMMAND), amount_step)],
        CUSTOM_GOAL: [MessageHandler(filters.TEXT & (~filters.COMMAND), custom_goal_step)],
        AMOUNT: [MessageHandler(filters.TEXT & (~filters.COMMAND), rate_step)],
        RATE: [MessageHandler(filters.TEXT & (~filters.COMMAND), final_step)],
    },
    fallbacks=[CommandHandler("cancel", lambda u,c: ConversationHandler.END)],
)
