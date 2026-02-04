import random
import string
from pyrogram import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import POST_MAP, MAX_BATCH_SIZE, AUTOPOST_WORKER
from database import save_batch

# Unique ID banane ke liye function
def generate_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def auto_post_job(client):
    """Ye function har interval par chalega"""
    for db_channel, target_channels in POST_MAP.items():
        # 1. Random Batch Size (1 se MAX_BATCH_SIZE tak)
        batch_size = random.randint(1, MAX_BATCH_SIZE)
        
        # 2. Random Message IDs pick karein (Assumption: IDs 1-5000)
        # Real world mein aap channel ki history se IDs nikal sakte hain
        random_ids = [random.randint(1, 5000) for _ in range(batch_size)]
        
        # 3. Batch ko Database mein save karein
        batch_id = generate_id()
        await save_batch(batch_id, random_ids)
        
        # 4. Target Channels mein post karein
        for target in target_channels:
            try:
                # Main Bot ka username chahiye link banane ke liye
                bot_username = (await client.get_me()).username
                link = f"https://t.me/{bot_username}?start=batch_{batch_id}"
                
                text = (
                    f"🎁 **NEW RANDOM BATCH**\n\n"
                    f"📦 Size: {batch_size} Videos\n"
                    f"⏳ Validity: 20 Hours\n\n"
                    f"Niche diye gaye link par click karke poora batch dekhein!"
                )
                
                # Dedicated Worker Bot se post karein
                await client.send_message(
                    chat_id=target,
                    text=text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📂 Watch Batch Now", url=link)]
                    ])
                )
            except Exception as e:
                print(f"Auto-post error for {target}: {e}")

# Scheduler setup
scheduler = AsyncIOScheduler()

# Maan lijiye har 2 ghante mein post karna hai (interval badal sakte hain)
# Note: Humne yahan 'client' pass kiya hai jo main.py se aayega
def start_scheduler(client):
    scheduler.add_job(auto_post_job, "interval", hours=2, args=[client])
    scheduler.start()
