import requests
import time
import os
from pyrogram import filters, Client
from pyrogram.types import InputMediaPhoto

# Command handler for /gen
@Client.on_message(filters.command(['imagine', 'generate']))
async def generate_image(client, message):
    # Get the prompt from the command
    prompt = ' '.join(message.command[1:])
    prompt_encoded = prompt.replace(' ', '%20')  # Encode the prompt for URL compatibility

    # Send a message to inform the user to wait
    wait_message = await message.reply_text("Please wait while I generating the images...")
    StartTime = time.time()

    # API endpoint URL with direct parameters
    url = f"https://death-image.ashlynn.workers.dev/?prompt={prompt_encoded}&image=6&dimensions=square&safety=false"

    try:
        # Send a GET request to the API
        response = requests.get(url)

        if response.status_code == 200:
            response_json = response.json()
            images = response_json.get("images", [])

            if images:
                media_group = []  # List to hold InputMediaPhoto objects
                temp_files = []   # Temporary list to track downloaded files

                # Download and save each image
                for idx, image_url in enumerate(images):
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        destination_path = f'generated_image_{idx + 1}.jpg'

                        with open(destination_path, 'wb') as f:
                            f.write(image_response.content)

                        # Add the image to the media group
                        media_group.append(InputMediaPhoto(media=open(destination_path, 'rb')))
                        temp_files.append(destination_path)

                # Send all images as a media group
                if media_group:
                    await client.send_media_group(
                        chat_id=message.chat.id,
                        media=media_group
                    )

                # Remove the temporary files after sending
                for file_path in temp_files:
                    os.remove(file_path)

                # Delete the wait message after sending all images
                await wait_message.delete()
            else:
                await wait_message.edit_text("No images returned by the API.")
        else:
            await wait_message.edit_text(f"API Error: {response.status_code}Give An Input!!\nᴜsᴇ - /imagine your prompt")

    except Exception as e:
        await wait_message.edit_text(f"Error: {e}")

