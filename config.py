import os

# --- [ CORE SETTINGS ] ---
# Inhe Koyeb Dashboard mein Environment Variables mein add karein
API_ID = int(os.environ.get("API_ID", "1234567"))
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_main_bot_token")

# --- [ WORKER BOTS ] ---
# Space-separated tokens in Koyeb: "token1 token2"
raw_forwarders = os.environ.get("WORKER_TOKENS", "")
FORWARD_WORKERS = raw_forwarders.split() if raw_forwarders else []

# Dedicated bot for Auto-Posting tasks
AUTOPOST_WORKER = os.environ.get("AUTOPOST_WORKER", "your_autopost_bot_token")

# --- [ DATABASE ] ---
# MongoDB Connection String from MongoDB Atlas
MONGO_URI = os.environ.get("MONGO_URI", "your_mongodb_uri_here")

# --- [ FSUB & SECURITY ] ---
# List of channel usernames that users MUST join
FSUB_CHANNELS = ["@AkMovieVerse"] 

# Range for the Math Captcha ($x + y = ?$)
CAPTCHA_RANGE = (1, 20)

# --- [ EARNING & VERIFICATION ] ---
# Your Shortlink domain and API Key
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "vplink.in")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "a236cdf68649bcdf6eaba5f1119eacac803ba4eb")

# How many hours until verification expires?
VERIFY_EXPIRE_HOURS = int(os.environ.get("VERIFY_EXPIRE_HOURS", "20"))
# Points rewarded per minute while in the Earning Section
PASSIVE_POINTS_PER_MIN = 1.5

# --- [ BATCH & AUTO-POST MAPPING ] ---
# Maximum number of files in a "True Random" batch
MAX_BATCH_SIZE = int(os.environ.get("MAX_BATCH_SIZE", "50"))

# Mapping: { "Database_Channel_ID": [Target_Channel_IDs] }
POST_MAP = {
    -1003617955958: [-1003895076121], 
    -1003563044650: [-1003786040332]
}

# 🟢 YE LINE ADD KAR DI HAI (ImportError Fix)
DB_CHANNELS = list(POST_MAP.keys())

# --- [ ADMIN SETTINGS ] ---
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8252482448"))
