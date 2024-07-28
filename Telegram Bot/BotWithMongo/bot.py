from typing import Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

from mongo_client import ExpenseMongoClient

BOT_TOKEN: Final = "<BOT_TOKEN>"
# connect to your mongodb
db_client = ExpenseMongoClient("localhost", 27017)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_expense_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    amount = int(context.args[0])
    category = context.args[1]
    description = " ".join(context.args[2:])

    db_client.add_expense(user_id=user_id, amount=int(amount), category=str(category), description=str(description))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Expense added successfully!",
        reply_to_message_id=update.effective_message.id,
    )


async def get_expenses_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id

    if context.args:
        category = context.args[0]
        expenses = db_client.get_expenses_by_category(user_id, category)
    else:
        expenses = db_client.get_expenses(user_id)
    text = "Your expenses are:\n"
    for expense in expenses:
        text += (
            f"{expense['amount']} - {expense['category']} - {expense['description']}\n"
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def get_categories_command_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    categories = db_client.get_categories(user_id)
    text = f"Your categories are: {', '.join(categories)}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    total = db_client.get_total_expense(user_id)
    text = f"Your total expense is: {total}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_by_category_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    total_by_category = db_client.get_total_expense_by_category(user_id)
    text = "Your total expenses by category are:\n"
    for category, expense in total_by_category.items():
        text += f"{category}: {expense}\n"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


if __name__ == "__main__":
    expense_mongo_client = ExpenseMongoClient("localhost", 27017)
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    # add all your handlers here
    bot.add_handler(CommandHandler("add_expense", add_expense_command_handler))
    bot.add_handler(CommandHandler("get_expenses", get_expenses_command_handler))
    bot.add_handler(CommandHandler("get_categories", get_categories_command_handler))
    bot.add_handler(CommandHandler("get_total_expense", get_total_expense_command_handler))
    bot.add_handler(CommandHandler("get_total_expense_by_category", get_total_expense_by_category_command_handler, ))

    # start bot
    bot.run_polling()
