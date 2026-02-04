import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import FSUB_CHANNELS, CAPTCHA_RANGE, POST_MAP
from database import get_user, add_points, update_verify_status, is_user_verified, get_batch

# Temporary storage for captcha and referral tracking
captcha_db = {} 

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    text = message.text
    
    # 1. Database mein user check/create karo
    user = await get_user(user_id)

    # --- [ BATCH LINK HANDLING ] ---
    if "batch_" in text:
        batch_id = text.split("batch_")[1]
        
        # Check if 20-hour verification is still valid
        verified = await is_user_verified(user_id)
        if not verified:
            return await message.reply_text(
                "🔒 **Content Locked!**\n\nIs batch ko dekhne ke liye aapko verify karna hoga. Verification 20 ghante tak valid rahegi.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔗 Verify & Unlock", callback_data="earn_menu")]
                ])
            )
        
        # If verified, fetch and send batch
        batch_data = await get_batch(batch_id)
        if batch_data:
            await message.reply_text(f"✅ Verified! Sending {len(batch_data['files'])} files...")
            # DB Channel ID pick karein (config se pehla DB channel default le rahe hain)
            db_channel = list(POST_MAP.keys())[0]
            for msg_id in batch_data['files']:
                try:
                    await client.copy_message(user_id, from_chat_id=db_channel, message_id=msg_id)
                    await asyncio.sleep(1) # Flood protection
                except: continue
        else:
            await message.reply_text("❌ Batch expire ho gaya ya nahi mila.")
        return

    # --- [ REFERRAL TRACKING ] ---
    text_parts = text.split()
    if len(text_parts) > 1 and not user.get("referred_by") and "batch_" not in text:
        ref_id = text_parts[1]
        if ref_id.isdigit() and int(ref_id) != user_id:
            captcha_db[user_id] = {"ref_id": int(ref_id)}

    # --- [ MULTI-FORCE SUBSCRIBE CHECK ] ---
    for channel in FSUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{channel[1:]}")]]
            buttons.append([InlineKeyboardButton("Verify Joining 🔄", url=f"https://t.me/{client.me.username}?start=resend")])
            return await message.reply_text(
                f"❌ **Access Denied!**\n\nApko hamare channels join karne honge use karne ke liye.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            pass 

    # --- [ MATH CAPTCHA ] ---
    if not user.get("is_verified"):
        n1 = random.randint(CAPTCHA_RANGE[0], CAPTCHA_RANGE[1])
        n2 = random.randint(CAPTCHA_RANGE[0], CAPTCHA_RANGE[1])
        ans = n1 + n2
        
        if user_id not in captcha_db: captcha_db[user_id] = {}
        captcha_db[user_id]["ans"] = ans
        
        return await message.reply_text(
            f"🛡️ **Security Check**\n\nProve karein ki aap human hain:\n**{n1} + {n2} = ?**\n\nJawab reply mein likhein."
        )

    # --- [ MAIN MENU ] ---
    # Agar user ke 50+ points hain toh VIP Choice button dikhao
    main_buttons = [
        [InlineKeyboardButton("💰 Earning Section", callback_data="earn_menu")],
        [InlineKeyboardButton("🎁 Daily Reward", callback_data="daily_reward")],
        [InlineKeyboardButton("👤 My Profile", callback_data="profile")]
    ]
    
    if user.get("points", 0) >= 50:
        main_buttons.append([InlineKeyboardButton("💎 VIP Content (Choice)", callback_data="vip_choice")])

    await message.reply_text(
        f"👋 Welcome {user_name}!\n\nAapka account active hai. Niche diye gaye options use karein.",
        reply_markup=InlineKeyboardMarkup(main_buttons)
    )

@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def captcha_checker(client, message):
    user_id = message.from_user.id
    if user_id in captcha_db and "ans" in captcha_db[user_id]:
        try:
            if int(message.text) == captcha_db[user_id]["ans"]:
                await update_verify_status(user_id)
                
                # Referral Points Delivery
                ref_id = captcha_db[user_id].get("ref_id")
                if ref_id:
                    await add_points(ref_id, 10)
                    await client.send_message(ref_id, "🎉 Naye user ne join kiya! +10 Points.")
                
                del captcha_db[user_id]
                await message.reply_text("✅ Verified! Dubara /start dabayein menu ke liye.")
            else:
                await message.reply_text("❌ Galat jawab. Phir se try karein.")
        except:
            pass
