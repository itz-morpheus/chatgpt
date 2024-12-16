import requests
from pyrogram import Client, filters
from pyrogram.types import *

@Client.on_message(filters.command(["instadl", "insdl", "insta", "instadownload"]))
async def igdownload(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please Provide an Instagram URL 🤦‍♂️\nlike this - /insta {ᴠɪᴅᴇᴏ_ᴜʀʟ}**")
    
    url = message.text.split(None, 1)[1]
    msg = await message.reply_text("**Downloading 📤**")
    
    # New API endpoint
    response = requests.get(f"https://api.paxsenix.biz.id/dl/ig?url={url}")
    data = response.json()
    
    if not data.get("ok", False):  # Check if API returned a valid response
        await message.reply_text("**Not a valid Instagram URL 🤷‍♂️**")
        await msg.delete()
        return

    result = data["url"]  # Updated to use the new API response
    media = []
    
    for item in result:
        if item["type"] == "photo":
            media.append(InputMediaPhoto(media=item["url"]))
        elif item["type"] == "video":
            media.append(InputMediaVideo(media=item["url"]))
    
    if media:
        await message.reply_media_group(media=media)  # Send media group
    else:
        await message.reply_text("**No media found in the URL provided 🤷‍♂️**")
    
    await msg.delete()
