import requests
import time
import os
from pyrogram import filters, Client

# Command handler for /gen
@Client.on_message(filters.command(['dechore', 'anime']))
async def generate_image(client, message):
    # Get the prompt from the command
    prompt = ' '.join(message.command[1:])
    prompt_encoded = prompt.replace(' ', '%20')  # Encode the prompt for URL compatibility
    
    # Send a message to inform the user to wait
    wait_message = await message.reply_text("Please wait while I generate the image...")
    StartTime = time.time()

    # API endpoint URL with direct parameters
    url = f"https://death-image.ashlynn.workers.dev/?prompt={prompt_encoded}&image=3&dimensions=tall&safety=false"
    
    try:
        # Send a GET request to the API
        response = requests.get(url)
        
        if response.status_code == 200:
            response_json = response.json()
            images = response_json.get("images", [])
            
            if images:
                # Download and save each image
                sent_images = []
                for idx, image_url in enumerate(images):
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        destination_path = f'generated_image_{idx + 1}.jpg'
                        
                        with open(destination_path, 'wb') as f:
                            f.write(image_response.content)
                        
                        # Send the image
                        sent_images.append(destination_path)
                        await client.send_photo(
                            message.chat.id,
                            photo=destination_path,
                            caption=f"Generated Image {idx + 1}:\nTime Taken: {time.time() - StartTime:.2f} seconds"
                        )
                        
                        # Remove the image after sending
                        os.remove(destination_path)
                
                # Delete the wait message after sending all images
                await wait_message.delete()
            else:
                await wait_message.edit_text("No images returned by the API.")
        else:
            await wait_message.edit_text(f"API Error: {response.status_code}Give An Input!!\nᴜsᴇ - /dechore your prompt")
    
    except Exception as e:
        await wait_message.edit_text(f"Error: {e}")
