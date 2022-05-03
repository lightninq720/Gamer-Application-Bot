import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import os
import json
from cogs.settings import ApplyView

os.chdir("./")

with open("config.json") as f:
    data = json.load(f)
TOKEN = data["TOKEN"]

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(ApplyView())
            self.persistent_views_added = True

        print(f"Logged in as {self.user}!")

        await self.change_presence(status = nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="bedwarspractice.club"))

intents = nextcord.Intents.default()

intents.members = True
client = Bot(command_prefix = "nom!", intents = intents)

client.remove_command("help")

os.chdir("./")
for filename in os.listdir('./cogs'):   
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename} cog")


@client.command()
@commands.has_permissions(administrator=True)
async def app(ctx):
    embed = nextcord.Embed(title="Apply!", description="Click the button below to apply for the guild :)")
    await ctx.send(embed=embed, view=ApplyView())

client.run(TOKEN)

