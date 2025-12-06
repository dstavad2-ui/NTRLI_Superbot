import os, asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('session_test', API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("Hello — click the button:", buttons=[Button.inline("Click me", b"btn1")])

@client.on(events.CallbackQuery)
async def cb(event):
    await event.answer("You clicked!")  # acknowledge callback
    await event.edit("✅ Button clicked!")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Bot is running")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
