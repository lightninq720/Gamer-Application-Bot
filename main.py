import discord
import os
import json
from discord.ext import commands , tasks
from discord_slash import SlashCommand, SlashContext

os.chdir("./")

with open("config.json") as f:
    data = json.load(f)
TOKEN = data["TOKEN"]



intents = discord.Intents.default()

intents.members = True
client = commands.Bot(command_prefix = "cringe", intents = intents)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

client.remove_command("help")

os.chdir("./")
for filename in os.listdir('./cogs'):   
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename} cog")



@client.event
async def on_ready():
    print ("Rain Guild Bot Ready")

    print(f"Logged in as {client.user}!")

    await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="Join rain"))


client.run(TOKEN)

