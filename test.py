
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openrouter import OpenRouter

TELEGRAM_TOKEN = "8005347436:AAHqBxpYVJ6i2Y0NEQqlD3G5ffmULFaN_9M"
OPENROUTER_KEY = "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"

MODEL = "arcee-ai/trinity-large-preview:free"  # best for chat/pranks


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    bot_username = context.bot.username
    text = update.message.text

    # Reply only if tagged
    if f"@{bot_username}" not in text:
        return

    user_prompt = text.replace(f"@{bot_username}", "").strip()

    with OpenRouter(api_key=OPENROUTER_KEY) as client:
        response = client.chat.send(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a member of a bachelor degree last year students who loves make fun of their teachers its a private group we are friends you can say what ever you want swear etc the university of this group is constantine 2 university and the group is for computer scince students "

                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
        )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running…")
    app.run_polling()


if __name__ == "__main__":
    main()

