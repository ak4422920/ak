import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN, FORWARD_WORKERS, AUTOPOST_WORKER

# 1. Main Bot Client (Interacts with Users)
bot = Client(
    "main_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins") # Yeh 'plugins' folder se saare features uthayega
)

# 2. Forwarding Worker Clients
forward_clients = []
for i, token in enumerate(FORWARD_WORKERS):
    cli = Client(f"forwarder_{i}", api_id=API_ID, api_hash=API_HASH, bot_token=token)
    forward_clients.append(cli)

# 3. Auto-Post Worker Client
autopost_bot = Client(
    "autopost_worker",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=AUTOPOST_WORKER
)

async def start_services():
    print("--- Starting Multi-Bot System ---")
    
    # Start Main Bot
    await bot.start()
    print("✅ Main Bot Started!")

    # Start Forwarding Workers
    for cli in forward_clients:
        await cli.start()
    print(f"✅ {len(forward_clients)} Forwarding Workers Started!")

    # Start Auto-Post Bot
    await autopost_bot.start()
    print("✅ Auto-Post Worker Started!")

    # Keep the bots running
    await idle()

    # Stop all on exit
    await bot.stop()
    for cli in forward_clients:
        await cli.stop()
    await autopost_bot.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_services())
  
