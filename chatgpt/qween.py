import requests
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("qwenai"))
async def ask(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Give an input!\nUsage: `/live your question`")
        return
    
    query = " ".join(message.command[1:])
    loading_msg = await message.reply_text("⚡ Processing your request...")
    
    api_url = f"https://api-y5s2.onrender.com/ashlynn?question={query}&model=qwen-coder"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()
        
        if data.get("status") == 200 and data.get("successful") == "success":
            api_response = data.get("response", "No response found.")
            await loading_msg.edit(
                f"👋 **Hey** {message.from_user.mention},\n\n"
                f"**Result:**\n{api_response}\n\n"
                f"🌐 [Join AR]({data.get('Join', '#')})"
            )
        else:
            await loading_msg.edit("⚠️ API returned an unexpected response. Please try again.")
    except requests.RequestException as e:
        await loading_msg.edit(f"❌ An error occurred while fetching the data:\n`{str(e)}`")
    except Exception as e:
        await loading_msg.edit(f"⚠️ Something went wrong:\n`{str(e)}`")
