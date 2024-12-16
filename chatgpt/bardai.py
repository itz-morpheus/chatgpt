import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command(["claude", "claudeai", "bardai", "claudy"]))
async def bardandgemini(_: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give An Input!!\nᴜsᴇ - /claude your question")

    query = " ".join(message.command[1:])    
    txt = await message.reply_text("☁️")
    app = f"https://darkness.ashlynn.workers.dev/chat/?prompt={query}&model=claude-3-haiku-20240307"
    response = requests.get(app)
    data = response.json()
    api = data['response']
    await txt.edit(f"ʜᴇʏ: {message.from_user.mention}\n\nϙᴜᴇʀʏ: {query}\n\nʀᴇsᴜʟᴛ:\n\n{api}")
