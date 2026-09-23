import discord
from discord.ext import commands
from discord import app_commands
import user_stats
import logging
from dotenv import load_dotenv
import os

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "Here are yesterday's results:" in message.content and message.author.display_name == "Wordle":
        log_day(message)


@bot.tree.command(name="stats")
async def stats(interaction):
    await interaction.response.defer()
    name = interaction.user.display_name
    channel = interaction.channel
    if user_stats.user_exists(name) == False:
        await channel_scan(name, channel)    
    await interaction.followup.send(user_stats.check_stats(name))


def log_day(message):
    print("logged day")
    lines = message.clean_content.splitlines()
    for line in lines:
        if "@" in line:
            line = line.replace("👑 ", "")
            line = line.replace(" ", "")
            names = line.split("@")
            for i in range(0, len(names)):
                if i == 0:
                    continue
                stats = user_stats.default_stats()
                stats["played:"] = str(int(stats["played:"]) + 1)
                stats[names[0]] = str(int(stats[names[0]]) + 1)
                if user_stats.user_exists(names[i]):
                    user_stats.update_stats(names[i], stats)
                else:
                    continue


async def channel_scan(name, channel):
    stats = user_stats.default_stats()
    
    async for message in channel.history(limit=None):
        if (
        name in message.clean_content 
        and message.author.display_name == "Wordle" 
        and "👑" in message.clean_content
        ):
            #print(message.clean_content)
            lines = message.clean_content.splitlines()
            for line in lines:
                if name in line:
                    for stat in stats:
                        if stat in line:
                            stats[stat] = str(int(stats[stat]) + 1)
                            stats["played:"] = str(int(stats["played:"]) + 1)
    
    name = name.replace(" ", "")
    user_stats.create_user(name)
    user_stats.update_stats(name, stats)
    

bot.run(os.getenv("API_TOKEN"), log_handler=handler)
