import discord
from discord.ext import commands, tasks
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("No TOKEN found in environment variables. Please set the TOKEN variable.")

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
WEBSITE_URL = "https://rainserver.uk"  # Replace with your website
CHECK_INTERVAL = 300  # Check every 5 minutes
USER_ID = 452603675689615360  # Replace with the Discord user ID to notify

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_website():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(WEBSITE_URL) as response:
                if response.status != 200:
                    user = await bot.fetch_user(USER_ID)
                    await user.send(f"⚠️ Alert: {WEBSITE_URL} is down! Status code: {response.status}")
        except Exception as e:
            user = await bot.fetch_user(USER_ID)
            await user.send(f"⚠️ Alert: {WEBSITE_URL} is unreachable! Error: {str(e)}")

@bot.event
async def on_ready():
    print(f'Bot is ready: {bot.user.name}')
    check_website.start()

# Run the bot
bot.run(TOKEN)

