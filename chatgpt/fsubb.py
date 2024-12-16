from pyrogram import Client, filters, enums
from config import FSUB_ID

async def not_subscribed(client, message):    
    try:
        user = await client.get_chat_member(FSUB_ID, message.from_user.id)
    except Exception:
        pass
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False
