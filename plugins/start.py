import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import FSUB_CHANNELS, CAPTCHA_RANGE
from database import get_user, add_points, update_verify_status, is_user_verified

# Temporary storage for captcha answers (In-memory)
captcha_db = {} 

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # 1. Database mein user check/create karo
    user = await get_user(user_id)

    # 2. Check for Referral
    text_parts = message.text.split()
    if len(text_parts) > 1 and not user.get("referred_by") and user_id not in captcha_db:
        ref_id = text_parts[1]
        if ref_id.isdigit() and int(ref_id) != user_id:
            # Save referrer temporarily until captcha is solved
            captcha_db[user_id] = {"ref_id": int(ref_id)}

    # 3. Force Subscribe Check
    for channel in FSUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{channel[1:]}")]]
            buttons.append([InlineKeyboardButton("Verify Joining 🔄", url=f"https://t.me/{client.me.username}?start=verify")])
            return await message.reply_text(
                f"❌ **Access Denied!**\n\nApko hamare channels join karne honge use karne ke liye.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            pass # Agar bot admin nahi hai toh skip

    # 4. Math Captcha (Agar verified nahi hai)
    if not user.get("is_verified"):
        n1 = random.randint(CAPTCHA_RANGE[0], CAPTCHA_RANGE[1])
        n2 = random.randint(CAPTCHA_RANGE[0], CAPTCHA_RANGE[1])
        ans = n1 + n2
        
        # Store answer for checking
        if user_id not in captcha_db: captcha_db[user_id] = {}
        captcha_db[user_id]["ans"] = ans
        
        return await message.reply_text(
            f"🛡️ **Security Check**\n\nProve karein ki aap human hain:\n**{n1} + {n2} = ?**\n\nJawab reply mein likhein."
        )

    # 5. Main Menu (Agar sab clear hai)
    await message.reply_text(
        f"👋 Welcome {user_name}!\n\nAapka verification valid hai. Menu use karein.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 Earning Section", callback_data="earn_menu")],
            [InlineKeyboardButton("🎁 Daily Reward", callback_data="daily_reward")],
            [InlineKeyboardButton("👤 My Profile", callback_data="profile")]
        ])
    )

@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def captcha_checker(client, message):
    user_id = message.from_user.id
    
    if user_id in captcha_db and "ans" in captcha_db[user_id]:
        try:
            user_ans = int(message.text)
            if user_ans == captcha_db[user_id]["ans"]:
                # Correct! 
                await update_verify_status(user_id) # Mark as verified
                
                # Agar koi referral tha toh use points do
                ref_id = captcha_db[user_id].get("ref_id")
                if ref_id:
                    await add_points(ref_id, 10) # 10 points for referral
                    await client.send_message(ref_id, "🎉 Kisi ne aapke link se join kiya! Aapko 10 points mile.")
                
                del captcha_db[user_id]
                await message.reply_text("✅ Verification Successful! /start dabayein menu ke liye.")
            else:
                await message.reply_text("❌ Galat jawab! Phir se koshish karein.(Try Again)")
        except ValueError:
            await message.reply_text("🔢 Please sirf number bhejye.")
          
