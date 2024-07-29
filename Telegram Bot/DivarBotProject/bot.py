import json
from typing import Final

from telegram import (
    Update,
    InlineQueryResultPhoto,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
    InlineQueryHandler,
)

from mongo_client import AdsMongoClient

BOT_TOKEN: Final = "<BOT_TOKEN>"
#BOT_TOKEN: Final = json.load(open("../token.json"))["token"]

CATEGORY, PHOTO, DESCRIPTION = range(3)
# db connection
db_client = AdsMongoClient("localhost", 27017)
# add your user ids here, you can use @userinfobot to get your user id
# DO NOT REMOVE EXISTING IDs
dev_ids = [92129627, 987654321, 91003546]


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="سلام، من ربات ثبت آگهی هستم. برای قبت آگهی جدید از دستور /add_advertising استفاده کنید.",
        reply_to_message_id=update.effective_message.id,
    )


async def add_category_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id not in dev_ids:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="شما اجازه دسترسی به این دستور را ندارید.",
            reply_to_message_id=update.effective_message.id,
        )
        return

    category = ""

    for s in context.args:
        category += s
        category += " "

    category = category.strip()

    db_client.add_category(category=category)

    text = f"دسته بندی {category} با موفقیت اضافه شد."

    print(db_client.get_categories())

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def add_advertising_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    categories = db_client.get_categories()
    text = "لطفا از بین دسته بندی های زیر یکی را انتخاب کنید:\n" + "\n".join(categories)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )

    return CATEGORY


async def choice_category_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["category"] = update.effective_message.text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="لطفا عکس آگهی خود را ارسال کنید.",
        reply_to_message_id=update.effective_message.id,
    )

    return PHOTO


async def photo_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["photo_url"] = update.effective_message.photo[-1].file_id

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="لطفا توضیحات آگهی خود را وارد کنید. در توضیحات می توانید اطلاعاتی مانند قیمت، شماره تماس و ... را وارد کنید.",
        reply_to_message_id=update.effective_message.id,
    )

    return DESCRIPTION


async def description_message_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    photo_url = context.user_data["photo_url"]
    category = context.user_data["category"]
    description = update.effective_message.text

    db_client.add_advertising(photo_url=photo_url, category=category, description=description, user_id=user_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="آگهی شما با موفقیت ثبت شد.",
        reply_to_message_id=update.effective_message.id,
    )

    return ConversationHandler.END


async def cancel_command_handler(
        update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="عملیات ثبت آگهی لغو شد. برای ثبت آگهی جدید از دستور /add_category استفاده کنید.",
        reply_to_message_id=update.effective_message.id,
    )

    return ConversationHandler.END


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command_handler))
    app.add_handler(CommandHandler("add_category", add_category_command_handler))
    app.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("add_advertising", add_advertising_command_handler)
            ],
            states={
                CATEGORY: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, choice_category_message_handler
                    )
                ],
                PHOTO: [
                    MessageHandler(filters.PHOTO, photo_message_handler),
                ],
                DESCRIPTION: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, description_message_handler
                    )
                ],
            },
            fallbacks=[
                CommandHandler("cancel", cancel_command_handler),
            ],
            allow_reentry=True,
        )
    )
    app.run_polling()
