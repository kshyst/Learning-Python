from uuid import uuid4

import requests
from telegram import Update, InlineQueryResultPhoto
import logging
import json
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext, MessageHandler, Updater, \
    filters, InlineQueryHandler

token = json.load(open("token.json"))["token"]
omdb = json.load(open("token.json"))["omdb"]

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


async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)


def delete_facts_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(name)
    if jobs:
        for job in jobs:
            job.schedule_removal()


async def facts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        a = int(context.args[0])
        if a < 10:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="please enter a number greater than 10")
            return
        job_name = str(update.effective_user.id)
        job_exists = delete_facts_job_if_exists(job_name, context)
        if job_exists:
            context.job_queue.run_repeating(
                job_facts_handler,
                interval=a,
                chat_id=update.effective_chat.id,
                name=job_name,
            )
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="your previous job were delete and you will receive a fact every {} seconds".format(
                                               a))
        else:
            context.job_queue.run_repeating(
                job_facts_handler,
                interval=a,
                chat_id=update.effective_chat.id,
                name=job_name
            )
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="you will receive a fact every {} seconds".format(
                                               a))
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="please enter a number greater than 10 not anything else")


async def unset_facts_job_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name(str(update.effective_user.id))
    for job in jobs:
        job.schedule_removal()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="you will no more receive facts")


async def job_facts_handler(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
    fact = data.json()["text"]
    await context.bot.send_message(chat_id=job.chat_id, text=fact)


logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    data = requests.get("https://thronesapi.com/api/v2/Characters")
    data = data.json()
    characters = {}
    for character in data:
        characters[character["fullName"]] = character["imageUrl"]
    if not query:
        results = []

        for name, url in characters.items():
            newItem = InlineQueryResultPhoto(
                id=str(uuid4()),
                photo_url=url,
                thumbnail_url=url,
                caption=name
            )
            results.append(newItem)
    else:
        results = []
        for name, url in characters.items():
            if query in name:
                newItem = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=url,
                    thumbnail_url=url,
                    caption=name
                )
                results.append(newItem)
    await update.inline_query.answer(results, auto_pagination=True)


if __name__ == "__main__":
    print(token)
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("ask", poll))
    application.add_handler(CommandHandler(["fact", "f"], fact))
    application.add_handler(CommandHandler("facts", facts_handler))
    application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    application.add_handler(CommandHandler("unset", unset_facts_job_handler))
    application.add_handler(InlineQueryHandler(inline_query))
    application.run_polling()
