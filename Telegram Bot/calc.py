import json
from typing import Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

BOT_TOKEN: Final = json.load(open("token.json"))["token"]


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n = int(context.args[0])
    m = int(context.args[1])
    adder = n + m
    text = str(n) + " + " + str(m) + " = " + str(adder)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id
    )


async def multiplication_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    n = int(context.args[0])
    m = int(context.args[1])
    adder = n * m
    text = str(n) + " * " + str(m) + " = " + str(adder)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id
    )


async def calculate_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    elements = []

    i = 0

    for arg in context.args:
        elements.append(str(arg))

    finalString = ""

    for e in elements:
        finalString += str(e) + " "

    finalAnswer = eval(finalString)

    text = finalString + "= " + str(finalAnswer)


    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id
    )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    # add all your handlers here
    bot.add_handler(CommandHandler("add", add_command_handler))
    bot.add_handler(CommandHandler("mult", multiplication_command_handler))
    bot.add_handler(CommandHandler("calc", calculate_command_handler))
    # start bot
    bot.run_polling()
