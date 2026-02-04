import os

# --- [ CORE SETTINGS ] ---
# Get these from https://my.telegram.org
API_ID = int(os.environ.get("API_ID", "1234567"))
API_HASH = os.environ.get("API_HASH", "your_api_hash_here")

# Main Bot Token from @BotFather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_main_bot_token")

# --- [ WORKER BOTS ] ---
# In Koyeb, add WORKER_TOKENS as a space-separated string: "token1 token2"
raw_forwarders = os.environ.get("WORKER_TOKENS", "")
FORWARD_WORKERS = raw_forwarders.split() if raw_forwarders else []

# Dedicated bot for Auto-Posting tasks
AUTOPOST_WORKER = os.environ.get("AUTOPOST_WORKER", "your_autopost_bot_token")

# --- [ DATABASE ] ---
# MongoDB Connection String from MongoDB Atlas
MONGO_URI = os.environ.get("MONGO_URI", "your_mongodb_uri_here")

# --- [ FSUB & SECURITY ] ---
# List of channel usernames (including @) that users MUST join
FSUB_CHANNELS = ["@AkMovieVerse"] 

# Range for the Math Captcha (e.g., 1 + 1 to 20 + 20)
# $x + y = ?$
CAPTCHA_RANGE = (1, 20)

# --- [ EARNING & VERIFICATION ] ---
# Your Shortlink domain (e.g., shareus.io, gplinks.in)
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "vplink.in")
# Your API Key from the shortliner website
SHORTLINK_API = os.environ.get("SHORTLINK_API", "a236cdf68649bcdf6eaba5f1119eacac803ba4eb")

# How many hours until verification expires?
VERIFY_EXPIRE_HOURS = int(os.environ.get("VERIFY_EXPIRE_HOURS", "20"))

# Points rewarded per minute while in the Earning Section
PASSIVE_POINTS_PER_MIN = 1.5

# --- [ BATCH & AUTO-POST MAPPING ] ---
# Maximum number of files in a "True Random" batch (1 to MAX)
MAX_BATCH_SIZE = int(os.environ.get("MAX_BATCH_SIZE", "50"))

# Mapping: { "Database_Channel_ID": [Target_Channel_IDs] }
# Note: Use -100 prefix for channel IDs
POST_MAP = {
    -1003617955958: [-1003895076121], # DB 1 posts to 2 targets
    -1003563044650: [-1003786040332]                 # DB 2 posts to 1 target
}

# --- [ ADMIN SETTINGS ] ---
# Your personal Telegram ID (Get it from @MissRose_bot or @userinfobot)
ADMIN_ID = int(os.environ.get("ADMIN_ID", "8252482448"))
