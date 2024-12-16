from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from io import BytesIO
import base64
import time

@Client.on_message(filters.command(["enhance", "upscale"]))
async def enhance_photo(client: Client, message: Message):   
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Please reply to a photo to enhance it.")
        return

    replied = message.reply_to_message    
    media = await replied.download()  # Download the photo locally
    mes = await message.reply_text("`Enhancing the photo, please wait...`")

    try:
        # Step 1: Get the token
        token_response = requests.post("https://photoaid.com/en/tools/api/tools/token")
        token_response.raise_for_status()
        token_data = token_response.json()
        token = token_data.get("token")
        if not token:
            raise ValueError("Failed to retrieve token")

        # Step 2: Convert the image to base64
        with open(media, "rb") as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")

        # Step 3: Upload the image
        upload_payload = {
            "base64": base64_image,
            "token": token,
            "reqURL": "/ai-image-enlarger/upload"
        }
        upload_headers = {
            "Cookie": f"uuidtoken2={token};",
            "Accept-Language": "en-US",
            "Content-Type": "text/plain;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://photoaid.com",
            "Referer": "https://photoaid.com/en/tools/ai-image-enlarger"
        }
        upload_response = requests.post(
            "https://photoaid.com/en/tools/api/tools/upload",
            json=upload_payload,
            headers=upload_headers
        )
        upload_response.raise_for_status()
        upload_data = upload_response.json()
        request_id = upload_data.get("request_id")
        if not request_id:
            raise ValueError("Failed to retrieve request ID")

        # Step 4: Poll for the result
        status_data = None
        while True:
            time.sleep(2)  # Wait for 2 seconds
            status_payload = {
                "request_id": request_id,
                "reqURL": "/ai-image-enlarger/result"
            }
            status_response = requests.post(
                "https://photoaid.com/en/tools/api/tools/result",
                json=status_payload,
                headers=upload_headers
            )
            status_response.raise_for_status()
            status_data = status_response.json()
            if status_data.get("statusAPI") == "ready":
                break

        # Retrieve the enhanced image in Base64 format
        result_base64 = status_data.get("result")
        if not result_base64:
            raise ValueError("Failed to retrieve enhanced image")

        # Decode the Base64 image
        result_image_data = base64.b64decode(result_base64)
        enhanced_image = BytesIO(result_image_data)
        enhanced_image.seek(0)

        # Step 5: Send the enhanced image back to the user
        await message.reply_document(
            document=enhanced_image,
            file_name="enhanced_photo.jpg",
            caption="**Photo successfully enhanced!**"
        )
    except Exception as e:
        await message.reply(f"An error occurred while enhancing the photo: {e}")
    finally:
        await mes.delete()
