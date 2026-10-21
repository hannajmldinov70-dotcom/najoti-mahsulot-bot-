
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

TEXTS = {
    "ru": {
        "welcome": "🍞 Добро пожаловать в «Наҷоти маҳсулот»!\nСпасаем продукты — экономим деньги.",
        "menu": "Выберите раздел:",
        "buyer": "🛍 Раздел покупателя\nВыбирайте продукты со скидками 50–70%. Самовывоз.",
        "seller": "🏪 Раздел продавца\nДля подключения кафе, пекарни или магазина свяжитесь с нами.",
        "offers": "📦 Пока предложения загружаются. Скоро здесь появятся товары со скидками.",
        "help": "ℹ️ Помощь\nВыберите раздел в меню или напишите нам.",
        "contact": "📞 Контакты\nСвяжитесь с командой проекта через Telegram.",
    },
    "tg": {
        "welcome": "🍞 Ба «Наҷоти маҳсулот» хуш омадед!\nМаҳсулотро наҷот медиҳем — пулро сарфа мекунем.",
        "menu": "Бахшро интихоб кунед:",
        "buyer": "🛍 Бахши харидор\nМаҳсулотро бо тахфифи 50–70% интихоб кунед. Худгирӣ.",
        "seller": "🏪 Бахши фурӯшанда\nБарои пайваст кардани қаҳвахона, нонвойхона ё мағоза ба мо нависед.",
        "offers": "📦 Ҳоло пешниҳодҳо омода мешаванд. Ба наздикӣ маҳсулоти тахфифдор пайдо мешаванд.",
        "help": "ℹ️ Кӯмак\nБахшро аз меню интихоб кунед ё ба мо нависед.",
        "contact": "📞 Тамос\nБо дастаи лоиҳа тавассути Telegram тамос гиред.",
    },
}

def make_keyboard(lang):
    if lang == "tg":
        buttons = [
            ["🛍 Харидор", "🏪 Фурӯшанда"],
            ["📦 Пешниҳодҳо", "ℹ️ Кӯмак"],
            ["📞 Тамос", "🇷🇺 Русский"],
        ]
    else:
        buttons = [
            ["🛍 Покупатель", "🏪 Продавец"],
            ["📦 Смотреть предложения", "ℹ️ Помощь"],
            ["📞 Контакты", "🇹🇯 Тоҷикӣ"],
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.setdefault("lang", "ru")
    await update.effective_message.reply_text(
        TEXTS[context.user_data["lang"]]["welcome"],
        reply_markup=make_keyboard(context.user_data["lang"]),
    )
    await update.effective_message.reply_text(
        TEXTS[context.user_data["lang"]]["menu"]
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if not message or not message.text:
        return

    text = message.text.strip()
    lang = context.user_data.get("lang", "ru")

    if text == "🇹🇯 Тоҷикӣ":
        context.user_data["lang"] = "tg"
        await start(update, context)
        return

    if text == "🇷🇺 Русский":
        context.user_data["lang"] = "ru"
        await start(update, context)
        return

    choices = {
        "🛍 Покупатель": "buyer",
        "🛍 Харидор": "buyer",
        "🏪 Продавец": "seller",
        "🏪 Фурӯшанда": "seller",
        "📦 Смотреть предложения": "offers",
        "📦 Пешниҳодҳо": "offers",
        "ℹ️ Помощь": "help",
        "ℹ️ Кӯмак": "help",
        "📞 Контакты": "contact",
        "📞 Тамос": "contact",
    }

    key = choices.get(text)
    if key:
        await message.reply_text(TEXTS[lang][key])
    else:
        await message.reply_text(
            TEXTS[lang]["menu"],
            reply_markup=make_keyboard(lang),
        )

async def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Set it as an environment variable."
        )

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("offers", start))
    app.add_handler(CommandHandler("customer", start))
    app.add_handler(CommandHandler("partner", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("contact", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Наҷоти маҳсулот bot is starting...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
