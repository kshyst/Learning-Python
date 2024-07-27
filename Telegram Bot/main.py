from telegram import Update
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, Updater

token = '6556571128:AAEqJyqhPaDX1rXLNJqL8LhrsTLdrlAfqns'

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


logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("ask", poll))
    application.run_polling()
