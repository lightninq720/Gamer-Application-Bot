import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import asyncio
import json



class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("config.json") as f:
            configData = json.load(f)
            deletemessagechannels = configData["delete_messages_channel"]
            deletemessagelog = configData["delete_messages_channel_log"]
        if message.channel.id in deletemessagechannels:
            if not message.author.bot == True:
                logchannel = message.guild.get_channel(deletemessagelog)
                embed=nextcord.Embed(title="Application", description=f"{message.content[0:3500]}")
                await logchannel.send(f"Message from {message.author.mention}/{message.author.id} in {message.channel.mention}/{message.channel.id}", embed=embed)
            await message.delete()



def setup(client):
    client.add_cog(Events(client))
