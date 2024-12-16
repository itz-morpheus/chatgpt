from .paste import create_paste
from pyrogram.types import *
from config import FSUB_ID
from .fsubb import not_subscribed
from pyrogram import Client, filters
from HorridAPI import Mango

@Client.on_message(filters.command("claud"))
async def claude(client, message):
    if FSUB_ID and not await not_subscribed(client, message):
        invite_link = await client.create_chat_invite_link(int(FSUB_ID))
        buttons = [[InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ", url=invite_link.invite_link)]]
        text = f"Hey {message.from_user.mention}\n You are not joined this channel"
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        return 
    if len(message.command) < 2:
        return await message.reply_text("Please provide the query")
            
    reply = message.reply_to_message    
    if reply:
        query = f"Old conversation: {l.text}\n\nNew conversation: {message.text}"
    else:
        query = " ".join(message.command[1:])
    msg = await message.reply_text("🔍")
    mango = Mango()
    response = mango.chat.completions.create(
        model="claude-3.5-sonnet",      
        messages=[{"role": "user", "content": query}]
    )
    if len(response.text) > 3700:        
        result = await create_paste(response.text)  
        await msg.edit(result)       
    else:
        await msg.edit(response.text)
      
