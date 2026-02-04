import asyncio
from pyrogram import Client, filters
from config import FORWARD_WORKERS, POST_MAP

# Word Replace/Remove Dictionary
# Format: "Purana Word": "Naya Word" (Khali chhodne par delete ho jayega)
WORDS_TO_CLEAN = {
    "@OldChannel": "@MyNewBot",
    "Join for more": "",
    "http://t.me/junk": "https://t.me/yourlink"
}

# 1. Message Cleaning Function
def clean_caption(caption):
    if not caption:
        return ""
    new_caption = caption
    for old, new in WORDS_TO_CLEAN.items():
        new_caption = new_caption.replace(old, new)
    return new_caption

# 2. Live Forwarding Logic
# Yeh filter un saare channels ko monitor karega jo POST_MAP ki keys mein hain
@Client.on_message(filters.chat(list(POST_MAP.keys())) & ~filters.service)
async def live_forwarder(client, message):
    # Pata lagao kis target channel mein bhejna hai
    targets = POST_MAP.get(message.chat.id)
    if not targets:
        return

    # Caption saaf karo
    final_caption = clean_caption(message.caption or message.text)

    # Media Filter: Sirf Video aur Photos bhejni hain (Aap badal sakte hain)
    if not (message.video or message.photo or message.document):
        return

    for target_id in targets:
        try:
            # COPY_MESSAGE use karne se "Forwarded From" tag nahi aata
            await message.copy(
                chat_id=target_id,
                caption=final_caption
            )
            # Anti-Flood Delay: 2 second ka gap taaki Telegram ban na kare
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error forwarding to {target_id}: {e}")
