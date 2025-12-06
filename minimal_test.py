# minimal_test.py
from telethon import TelegramClient, events, Button
import os
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('sessions/test.session', API_ID, API_HASH)

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond(
        "Test menu:", 
        buttons=[[Button.inline("🔘 Press me", b"test_button")]]
    )

@client.on(events.CallbackQuery)
async def cb(event):
    print(">>> Callback received:", event.data)
    await event.answer()  # Must answer callback
    await event.respond(f"You pressed: {event.data.decode()}")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Test bot running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio; asyncio.run(main())
