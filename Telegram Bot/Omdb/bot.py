import json
from typing import Final

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    InlineQueryHandler,
)

from omdb_client import search_movie_by_title

BOT_TOKEN: Final = json.load(open("../token.json"))["token"]


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def search_movie_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    if query.__contains__("only_poster"):
        movies = search_movie_by_title(query.replace(" only_poster", ""))
        results = [
            InlineQueryResultPhoto(
                id=movie.imdb_id,
                caption=f"{movie.title} - {movie.year}",
                title=movie.title,
                thumbnail_url=movie.poster,
                photo_url=movie.poster,
            )
            for movie in movies
        ]
    else:
        movies = search_movie_by_title(query)
        results = [
            InlineQueryResultArticle(
                id=movie.imdb_id,
                title=movie.title,
                input_message_content=InputTextMessageContent(
                    message_text=f"{movie.title} - {movie.year}:\n\nhttps://www.imdb.com/title/{movie.imdb_id}"
                ),
                thumbnail_url=movie.poster,

            )
            for movie in movies
        ]

    await context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(InlineQueryHandler(search_movie_inline_query))
    bot.run_polling()
