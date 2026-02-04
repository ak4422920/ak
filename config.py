import os

# --- CORE SETTINGS ---
# My.telegram.org se milega
API_ID = int(os.environ.get("API_ID", "1234567")) 
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")

# @BotFather se milega
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_main_bot_token")

# --- WORKER SETTINGS ---
# Yahan apne alag-alag worker bots ke tokens daalo
FORWARD_WORKERS = ["token1", "token2"]
AUTOPOST_WORKER = "token3" 

# --- DATABASE ---
# MongoDB connection string
MONGO_URI = os.environ.get("MONGO_URI", "your_mongodb_uri")

# --- LOGIC SETTINGS ---
FSUB_CHANNELS = ["@Channel1", "@Channel2"] # Multi-FSub list
VERIFY_EXPIRE_HOURS = 20 # 20 ghante ka cooldown
BATCH_SIZE = 5 # Ek baar mein kitne videos ka batch milega
