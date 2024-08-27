from telethon.sessions import StringSession
from telethon.sync import TelegramClient, events


TOKEN = '7310054959:AAFCsMzHo9VSpeEbkmwLqqIpkKJ1lmHf_I8'
SESSION = 'session_123'


bot = TelegramClient('bot_session', api_id=123, api_hash='None').start(bot_token=TOKEN)

admin_id = [000]

tracked_users = []
monitored_chats = []
notify_chat_id = None


@bot.on(events.NewMessage(pattern='/start'))
async def start_bot(objects):
    await objects.reply('Бот Готов к работе.')



@bot.on(events.NewMessage(pattern='/add_user'))
async def add_user(objects):
    if objects.sender_id in admin_id:
        username = objects.message.message.split()[1]
        tracked_users.append(username)
        await objects.reply(f'@{username} Успешно добавлен!')


@bot.on(events.NewMessage(pattern='/remove_user'))
async def remove_user(objects):
    if objects.sender_id in admin_id:
        username = objects.message.message.split()[1]
        if username in tracked_users:
            tracked_users.remove(username)
            await objects.reply(f'@{username} Успешно удален!')
        else:
            await objects.reply(f'@{username} Не отслеживается.')


@bot.on(events.NewMessage(pattern='/add_chat'))
async def add_chat(objects):
    if objects.sender_id in admin_id:
        chat_id = objects.message.message.split()[1]
        if chat_id in monitored_chats:
            monitored_chats.append(chat_id)
            await objects.reply(f'@{chat_id} - добавление рабочего чата.')


@bot.on(events.NewMessage(pattern='/remove_chat'))
async def remove_chat(objects):
    if objects.sender_id in admin_id:
        chat_id = objects.message.message.split()[1]
        if chat_id in monitored_chats:
            monitored_chats.remove(chat_id)
            await objects.reply(f'@{chat_id} - удаление рабочего чата.')
        else:
            await objects.reply(f'@{chat_id} Не найден, Похоже что он был удален.')


@bot.on(events.NewMessage(pattern='/set_notify_chat'))
async def set_notify_chat(objects):
    global notify_chat_id
    if objects.sender_id in admin_id:
        notify_chat_id = int(objects.message.message.split()[1])
        await objects.reply(f'Чат {notify_chat_id} Установлен!')


@bot.on(events.NewMessage(chats=monitored_chats))
async def monitor_chats(event):
    sender = await event.get_sender()
    if sender.username in tracked_users:
        if notify_chat_id:
            message = f"Новый пост от @{sender.username} в чате {event.chat_id}:\n\n{event.message.message}"
            await bot.send_message(notify_chat_id, message)


bot.start()
bot.run_until_disconnected()
