import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import os
import json

os.chdir("./")

with open("config.json") as f:
    data = json.load(f)
TOKEN = data["TOKEN"]



intents = nextcord.Intents.default()

intents.members = True
client = commands.Bot(command_prefix = "cringe", intents = intents)

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

    await client.change_presence(status = nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="Join rain"))


client.run(TOKEN)

