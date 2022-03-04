import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import asyncio
import json

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="deletemessagechannel", description="base command")
    async def _deletemessagechannel(ctx: nextcord.Interaction):
        pass
    @_deletemessagechannel.subcommand(name="add", description="Add a delete message channel")
    async def _deletedmessagechannel_add(
        self,
        ctx: Interaction,
        channel : GuildChannel = SlashOption(
            name="channel",
            description="Channel to add to deleted message channels",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        )
    ):
        if not ctx.user.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", ephemeral=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        if channel.id in data["delete_messages_channel"]:
            await ctx.send("This channel is already added to auto delete.", ephemeral=True)
            return
        data["delete_messages_channel"].append(channel.id)
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=nextcord.Embed(title="Deleted message channel added", description=f"Successfully added {channel.mention} to the deleted message channels")
        await ctx.send(embed=embed)

    @_deletemessagechannel.subcommand(name="remove", description="Remove a delete message channel")
    async def _deletedmessagechannel_remove(
        self,
        ctx: Interaction,
        channel : GuildChannel = SlashOption(
            name="channel",
            description="Channel to remove from deleted message channels",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        )
    ):
        if not ctx.user.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", ephemeral=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        if channel.id not in data["delete_messages_channel"]:
            await ctx.send("This channel is not added to auto delete.", ephemeral=True)
            return
        index = data["delete_messages_channel"].index(channel.id)
        del data["delete_messages_channel"][index]
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=nextcord.Embed(title="Deleted message channel removed", description=f"Successfully removed {channel.mention} from the deleted message channels")
        await ctx.send(embed=embed)
    @_deletemessagechannel.subcommand(name="list", description="Get a list of the delete message channels")
    async def _deletedmessagechannel_list(
        self,
        ctx: Interaction,
    ):
        if not ctx.user.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", ephemeral=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        channels = ""
        for index, channel in enumerate(data["delete_messages_channel"]):
            channels = channels + f"{index+1}. <#{channel}>\n"
        embed=nextcord.Embed(title="Delete message channel list", description="{0}".format(channels))
        await ctx.send(embed=embed)
    @_deletemessagechannel.subcommand(name="log", description="Sets the delete message log channel")
    async def _deletedmessagechannel_log(
        self,
        ctx: Interaction,
        channel : GuildChannel = SlashOption(
            name="channel",
            description="Channel to use as the deleted message log channel",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        )
    ):
        if not ctx.user.guild_permissions.administrator == True:
            await ctx.send("You need `administrator` permissions to run this command", ephemeral=True)
            return
        with open("config.json") as f:
            data = json.load(f)
        data["delete_messages_channel_log"] = channel.id
        with open("config.json", "w") as f:
            json.dump(data, f)
        embed=nextcord.Embed(title="Deleted message log channel added", description=f"Successfully set the log channel to {channel.mention}")
        await ctx.send(embed=embed)






def setup(client):
    client.add_cog(Settings(client))
