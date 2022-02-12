import discord
from discord.ext import commands, tasks
import asyncio
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice

class Settings(commands.Cog):
    def __innit__(self, client):
        self.client = client

    @cog_ext.cog_subcommand(base="deletemessagechannel",
        name="add",
        description="Add a delete message channel",
        options=[
            create_option(
                name="channel",
                description="Channel to add to deleted message channels",
                option_type=discord.TextChannel,
                required=True
    )])
    async def _deletedmessagechannel_add(self, ctx, channel : discord.TextChannel):
        if not ctx.author.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", hidden=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        if channel.id in data["delete_messages_channel"]:
            await ctx.send("This channel is already added to auto delete.", hidden=True)
            return
        data["delete_messages_channel"].append(channel.id)
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=discord.Embed(title="Deleted message channel added", description=f"Successfully added {channel.mention} to the deleted message channels")
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="deletemessagechannel",
        name="remove",
        description="Remove a delete message channel",
        options=[
            create_option(
                name="channel",
                description="Channel to remove from deleted message channels",
                option_type=discord.TextChannel,
                required=True
    )])
    async def _deletedmessagechannel_remove(self, ctx, channel : discord.TextChannel):
        if not ctx.author.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", hidden=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        if channel.id not in data["delete_messages_channel"]:
            await ctx.send("This channel is not added to auto delete.", hidden=True)
            return
        index = data["delete_messages_channel"].index(channel.id)
        del data["delete_messages_channel"][index]
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=discord.Embed(title="Deleted message channel removed", description=f"Successfully removed {channel.mention} from the deleted message channels")
        await ctx.send(embed=embed)
    @cog_ext.cog_subcommand(base="deletemessagechannel",
        name="list",
        description="Get a list of the delete message channels"
    )
    async def _deletedmessagechannel_list(self, ctx):
        if not ctx.author.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", hidden=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        channels = ""
        for index, channel in enumerate(data["delete_messages_channel"]):
            channels = channels + f"{index+1}. <#{channel}>\n"
        embed=discord.Embed(title="Delete message channel list", description="{0}".format(channels))
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="deletemessagechannel",
        name="log",
        description="Sets the delete message log channel",
        options=[
            create_option(
                name="channel",
                description="Channel to use as the deleted message log channel",
                option_type=discord.TextChannel,
                required=True
    )])
    async def _deletedmessagechannel_log(self, ctx, channel : discord.TextChannel):
        if not ctx.author.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", hidden=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        data["delete_messages_channel_log"] = channel.id
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=discord.Embed(title="Deleted message log channel added", description=f"Successfully set the log channel to {channel.mention}")
        await ctx.send(embed=embed)





def setup(client):
    client.add_cog(Settings(client))