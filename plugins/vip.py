import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import users_col, add_points

# Database Channel IDs (Inhe apne hisab se badlein)
VIP_CHANNELS = {
    "movies": "https://t.me/+NuguHYCpQNplNjBi", # Movie DB Link
    "desi": "https://t.me/+ZbQ__vji70MwNTNi",   # Desi DB Link
    "foreign": "https://t.me/+gvAXt4A8giU1Njhi" # Foreign DB Link
}

@Client.on_callback_query(filters.regex("vip_choice"))
async def vip_menu(client, callback_query):
    text = (
        "💎 **VIP Exclusive Access**\n\n"
        "Aapke paas 50+ points hain! Niche di gayi categories mein se kisi ek ka access lein.\n\n"
        "⚠️ **Note:** Aapka access link sirf **3 minute** tak valid rahega, uske baad message auto-delete ho jayega!"
    )
    
    buttons = [
        [InlineKeyboardButton("🎬 Movies Pack", callback_data="get_vip_movies")],
        [InlineKeyboardButton("🇮🇳 Desi Special", callback_data="get_vip_desi")],
        [InlineKeyboardButton("🌍 Foreign Content", callback_data="get_vip_foreign")]
    ]
    
    await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r"get_vip_"))
async def deliver_vip(client, callback_query):
    user_id = callback_query.from_user.id
    category = callback_query.data.split("_")[-1] # movies, desi, ya foreign
    
    # 1. Deduct Points (Optional: Hum 50 points minus kar rahe hain access ke liye)
    user = await users_col.find_one({"user_id": user_id})
    if user.get("points", 0) < 50:
        return await callback_query.answer("❌ Aapke points kam ho gaye hain!", show_alert=True)
    
    await add_points(user_id, -50) # 50 points kaat liye
    
    # 2. Get the link
    vip_link = VIP_CHANNELS.get(category)
    
    # 3. Send the self-destructing message
    sent_msg = await client.send_message(
        user_id,
        f"✅ **{category.upper()} VIP Access Unlocked!**\n\n"
        f"🔗 **Link:** {vip_link}\n\n"
        f"⏰ Yeh message **1 minute** mein delete ho jayega. Jaldi join karein!"
    )
    
    await callback_query.answer(f"Success! {category} link sent.", show_alert=True)
    await callback_query.message.delete() # Old menu delete karo

    # 4. Timer to Delete (The Self-Destruct Logic)
    await asyncio.sleep(60) # 180 seconds = 3 minutes
    try:
        await sent_msg.delete()
        await client.send_message(user_id, "⌛ VIP link expire ho gaya aur delete kar diya gaya hai.")
    except:
        pass # Agar user ne pehle hi delete kar diya ho
