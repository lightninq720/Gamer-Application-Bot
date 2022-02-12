import discord
from discord.ext import commands, tasks
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component


with open("config.json") as f:
    configData = json.load(f)
    deletemessagechannels = configData["delete_messages_channel"]
    deletemessagelog = configData["delete_messages_channel_log"]


class Events(commands.Cog):
    def __innit__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in deletemessagechannels:
            logchannel = message.guild.get_channel(deletemessagelog)
            await logchannel.send(f"{message.channel.mention}\n\n{message.content[0:1950]}")
            await message.delete()



def setup(client):
    client.add_cog(Events(client))
