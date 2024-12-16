import requests
from pyrogram import Client, filters
from pyrogram.types import InputMediaVideo
import re
import asyncio

@Client.on_message(filters.command(["snapstories", "snapstory"]))
async def fetch_snap_story(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide a Snapchat username or profile URL 🤦‍♂️\nlike this - /snap {username or profile URL}**")

    user_input = message.text.split(None, 1)[1]

    # Extract username if input is a profile URL
    if "snapchat.com/add/" in user_input:
        match = re.search(r"snapchat\.com/add/([\w.]+)", user_input)
        if match:
            username = match.group(1)
        else:
            return await message.reply_text("**Invalid Snapchat profile URL 🤷‍♂️**")
    else:
        username = user_input.strip()

    msg = await message.reply_text("**Fetching stories... 📤**")

    # API endpoint for fetching stories
    api_url = f"https://snap-api.ashlynn.workers.dev/get_story/{username}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if not data.get("status"):
            await msg.edit("**No stories found or invalid username 🤷‍♂️**")
            return

        # Extract media URLs
        media_urls = data.get("data", [])

        if not media_urls:
            await msg.edit("**No media available in the user's story 🤷‍♂️**")
            return

        # Function to send media concurrently, 5 at a time
        async def send_media_concurrently(urls):
            sem = asyncio.Semaphore(5)  # Limit to 5 concurrent requests

            async def send_video(url):
                async with sem:
                    try:
                        await client.send_video(chat_id=message.chat.id, video=url)
                    except Exception as e:
                        print(f"Error sending video: {e}")

            tasks = [send_video(url) for url in urls]
            await asyncio.gather(*tasks)

        # Send all media URLs concurrently
        await send_media_concurrently(media_urls)
        await msg.delete()
    except requests.exceptions.RequestException as e:
        await msg.edit(f"**Failed to fetch stories: {str(e)}**")
