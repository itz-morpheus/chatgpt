import os
import requests
from pyrogram import Client, filters

api = "https://api.kenliejugarap.com/pixtral-paid/"

@Client.on_message(filters.command("scan_ph"))
async def scan_ph(client, message):
    try:
        # Ensure the command is used in reply to a photo
        reply = message.reply_to_message
        if not reply:
            return await message.reply_text("❌ **Reply to a photo to use this command!**")
        elif not reply.photo:
            return await message.reply_text("❌ **Reply to a photo to use this command!**")
        elif reply.video:
            return await message.reply_text("❌ **This command is only for photos, not videos!**")

        # Parse the query
        query = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
        if not query:
            await message.reply("❌ **Provide a query! Use `/scan_ph <query>` format.**")
            return

        # Notify the user about processing
        k = await message.reply_text(f"🔄 **Checking your image, {message.from_user.mention}... Please wait.**")

        # Download the replied photo
        media_path = await reply.download()

        # Upload the image to tmpfiles.org
        upload_url = "https://tmpfiles.org/api/v1/upload"
        with open(media_path, "rb") as file:
            upload_response = requests.post(upload_url, files={"file": file})

        # Validate the upload response
        if upload_response.status_code != 200 or "data" not in upload_response.json():
            await k.edit("❌ **Failed to upload the image. Please try again later.**")
            return

        # Get the direct image URL from tmpfiles.org
        upload_data = upload_response.json()
        img_url = upload_data["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")

        # Make a request to the external API with the image URL and query
        response = requests.get(f"{api}?question={query}&image_url={img_url}")
        
        if response.status_code == 200:
            # Process the API response
            result = response.json()
            await k.edit(f"✅ **Result for your query, {message.from_user.mention}:**\n\n{result['response']}")
        else:
            await k.edit("❌ **Failed to process your request. Please try again later.**")

        # Clean up the downloaded image file
        os.remove(media_path)

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error: {e}")
        await message.reply_text(f"❌ **An unexpected error occurred: {str(e)}**")
