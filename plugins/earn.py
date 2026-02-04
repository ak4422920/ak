import time
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SHORTLINK_URL, SHORTLINK_API, PASSIVE_POINTS_PER_MIN
from database import get_user, add_points, update_verify_status

# Timer track karne ke liye (User ID: Start Time)
earning_sessions = {}

@Client.on_callback_query(filters.regex("earn_menu"))
async def earn_menu(client, callback_query):
    user_id = callback_query.from_user.id
    
    # Secret Timer Start: User ne earning section open kiya
    earning_sessions[user_id] = time.time()
    
    # Shortlink generate karna (Aapki API key se)
    # Token format: verify_{user_id}_{timestamp}
    token = f"verify_{user_id}_{int(time.time())}"
    api_url = f"https://{SHORTLINK_URL}/api?api={SHORTLINK_API}&url=https://t.me/{client.me.username}?start={token}"
    
    try:
        res = requests.get(api_url).json()
        short_url = res["shortenedUrl"]
    except:
        short_url = "https://google.com" # Fallback agar API down ho

    text = (
        "💰 **Earning Section**\n\n"
        "Niche diye gaye button par click karke verify karein aur points kamaein.\n\n"
        "⚠️ **Note:** Verification ke baad hi points aapke account mein add honge."
    )
    
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Verify Shortlink", url=short_url)],
            [InlineKeyboardButton("🔄 Refresh / Check Status", callback_data="check_earn")]
        ])
    )

@Client.on_message(filters.regex(r"verify_") & filters.private)
async def verify_handler(client, message):
    user_id = message.from_user.id
    
    # 1. Check if user was in earning session
    if user_id in earning_sessions:
        start_time = earning_sessions[user_id]
        end_time = time.time()
        
        # Calculation: Kitne minute spend kiye?
        minutes_spent = round((end_time - start_time) / 60, 2)
        if minutes_spent > 60: minutes_spent = 60 # Limit 1 hour to prevent abuse
        
        passive_points = minutes_spent * PASSIVE_POINTS_PER_MIN
        total_reward = 20 + passive_points # 20 Base points + Timer points
        
        # 2. Update Database
        await add_points(user_id, total_reward)
        await update_verify_status(user_id)
        
        # Session khatam
        del earning_sessions[user_id]
        
        await message.reply_text(
            f"✅ **Verification Complete!**\n\n"
            f"Base Reward: 20 Points\n"
            f"Time Bonus ({minutes_spent} min): {passive_points:.1f} Points\n"
            f"**Total Received: {total_reward:.1f} Points**"
        )
    else:
        await message.reply_text("❌ Session expired. Please menu se dubara try karein.")
