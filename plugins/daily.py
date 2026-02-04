import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from config import DB_CHANNELS
from database import users_col

@Client.on_callback_query(filters.regex("daily_reward"))
async def daily_handler(client, callback_query):
    user_id = callback_query.from_user.id
    user = await users_col.find_one({"user_id": user_id})
    
    # 1. 24-Hour Cooldown Check
    last_claim = user.get("last_daily_claim")
    if last_claim:
        if datetime.now() < last_claim + timedelta(hours=24):
            time_left = (last_claim + timedelta(hours=24)) - datetime.now()
            hours, remainder = divmod(int(time_left.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            return await callback_query.answer(
                f"⏳ Sabar karein! Agla reward {hours}h {minutes}m baad milega.", 
                show_alert=True
            )

    # 2. Pick Random Videos from Database
    if not DB_CHANNELS:
        return await callback_query.answer("❌ Admin ne abhi tak Database set nahi kiya!", show_alert=True)
    
    # Bot random message IDs pick karega (Assuming IDs 1 to 5000 ke beech hain)
    # Pro Tip: Is range ko aap apne hisab se badal sakte hain
    random_ids = [random.randint(1, 5000) for _ in range(3)] 
    db_chat = random.choice(DB_CHANNELS)

    await callback_query.message.edit_text("🎁 Aapka daily reward taiyaar ho raha hai...")

    # 3. Send Videos to User
    success_count = 0
    for msg_id in random_ids:
        try:
            # Message copy karna taaki "Forwarded" tag na aaye
            await client.copy_message(
                chat_id=user_id,
                from_chat_id=db_chat,
                message_id=msg_id
            )
            success_count += 1
        except Exception:
            continue # Agar woh ID khali hai toh skip

    if success_count > 0:
        # Update Database with new timestamp
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": {"last_daily_claim": datetime.now()}}
        )
        await client.send_message(user_id, f"✅ Aapko aaj ke {success_count} videos mil gaye hain! Kal phir aaiyega.")
    else:
        await callback_query.message.reply_text("❌ Kuch error aaya, please thodi der baad try karein.")
