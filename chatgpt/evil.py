import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram import Client, filters


@Client.on_message(filters.command(["evil", "evilai"]))
async def mixtral(_: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give An Input!!\nᴜsᴇ - /mixtral your question")

    query = " ".join(message.command[1:])    
    txt = await message.reply_text("😈")
    app = f"https://api-y5s2.onrender.com/ashlynn?question={query}&model=evil"
    response = requests.get(app)
    data = response.json()
    api = data['response']
    await txt.edit(f"ϙᴜᴇʀʏ: {query}\n\nʀᴇsᴜʟᴛ:\n\n{api}")
