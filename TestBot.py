from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

TOKEN = '7310054959:AAFCsMzHo9VSpeEbkmwLqqIpkKJ1lmHf_I8'

admin_ids = [000]

tracked_users = []
monitored_chats = []
notify_chat_id = None


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Бот готов к работе.')


async def add_user(update: Update, context: CallbackContext) -> None:
    try:
        username = context.args[0]
        if username not in tracked_users:
            tracked_users.append(username)
            await update.message.reply_text(f'@{username} успешно добавлен!')
        else:
            await update.message.reply_text(f'@{username} уже отслеживается.')
    except IndexError:
        await update.message.reply_text('Укажите имя пользователя для добавления.')


async def remove_user(update: Update, context: CallbackContext) -> None:
    try:
        username = context.args[0]
        if username in tracked_users:
            tracked_users.remove(username)
            await update.message.reply_text(f'@{username} успешно удален!')
        else:
            await update.message.reply_text(f'@{username} не отслеживается.')
    except IndexError:
        await update.message.reply_text('Укажите имя пользователя для удаления.')


async def add_chat(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = int(context.args[0])
        if chat_id not in monitored_chats:
            monitored_chats.append(chat_id)
            await update.message.reply_text(f'Чат {chat_id} добавлен.')
        else:
            await update.message.reply_text(f'Чат {chat_id} уже отслеживается.')
    except IndexError:
        await update.message.reply_text('Укажите ID чата для добавления.')
    except ValueError:
        await update.message.reply_text('Укажите правильный ID чата.')


async def remove_chat(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = int(context.args[0])
        if chat_id in monitored_chats:
            monitored_chats.remove(chat_id)
            await update.message.reply_text(f'Чат {chat_id} удален.')
        else:
            await update.message.reply_text(f'Чат {chat_id} не найден.')
    except IndexError:
        await update.message.reply_text('Укажите ID чата для удаления.')
    except ValueError:
        await update.message.reply_text('Укажите правильный ID чата.')


async def set_notify_chat(update: Update, context: CallbackContext) -> None:
    global notify_chat_id
    try:
        notify_chat_id = int(context.args[0])
        await update.message.reply_text(f'Чат {notify_chat_id} установлен для уведомлений.')
    except IndexError:
        await update.message.reply_text('Укажите ID чата для уведомлений.')
    except ValueError:
        await update.message.reply_text('Укажите правильный ID чата.')


async def monitor_chats(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username
    if username in tracked_users:
        if notify_chat_id:
            message = f"Новый пост от @{username} в чате {update.message.chat_id}:\n\n{update.message.text}"
            await context.bot.send_message(chat_id=notify_chat_id, text=message)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add_user', add_user))
    application.add_handler(CommandHandler('remove_user', remove_user))
    application.add_handler(CommandHandler('add_chat', add_chat))
    application.add_handler(CommandHandler('remove_chat', remove_chat))
    application.add_handler(CommandHandler('set_notify_chat', set_notify_chat))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, monitor_chats))

    application.run_polling()

if __name__ == '__main__':
    main()
