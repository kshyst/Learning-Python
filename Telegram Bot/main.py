from telegram import Update
import logging
import json
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, Updater, \
    filters

token = json.load(open("token.json"))["token"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi!')


async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.sendPoll(chat_id=update.effective_chat.id, question="are you a nigger ?", options=["yes", "no"])


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    due = float(context.args[0])
    context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
        reply_to_message_id=update.effective_message.id
    )


logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("ask", poll))
    application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    application.run_polling()
