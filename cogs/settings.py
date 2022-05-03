import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import asyncio
import json

class Settings(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @nextcord.slash_command(name="sendmessage", description="Send message")
    async def _sendmessage(ctx: Interaction):
        pass

    @_sendmessage.subcommand(name="sendmessagebutton", description="Send a message with a button")
    async def _sendmessagebutton(self, ctx: Interaction, channel: GuildChannel = SlashOption(name="channel", description="Channel to send message with button", required=True, channel_types=[nextcord.ChannelType.text])):
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You need `administrator` permissions to run this command", ephemeral=True)
            return

        def check(message):
            return message.author.id == ctx.user.id

        buttonMsg = await ctx.send("Which button to use?")

        try:    
            buttonName: nextcord.Message = await self.client.wait_for("message", timeout=30.0, check=check)

            if buttonName.content.lower() != "application":
                await ctx.send("Invalid button name", delete_after=3)
                raise asyncio.TimeoutError

            embedTitle = await ctx.send("Embed Title?")
            embedTitleUser: nextcord.Message = await self.client.wait_for("message", timeout=30.0, check=check)

            embedDesc = await ctx.send("Embed Description?")
            embedDescUser: nextcord.Message = await self.client.wait_for("message", timeout=30.0, check=check)
        
        except asyncio.TimeoutError:
            # await buttonMsg.delete()
            # await embedTitle.delete()
            # await embedDesc.delete()
            return
        
        # await buttonMsg.delete()
        # await embedTitle.delete()
        # await embedDesc.delete()

        embed = nextcord.Embed(title=embedTitleUser.content, description=embedDescUser.content)
        await channel.send(embed=embed, view=ApplyView())

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


class ApplyView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Apply!", style=nextcord.ButtonStyle.blurple, custom_id="apply_view:applying")
    async def apply(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        form = ApplyForm()
        await ctx.response.send_modal(modal=form)

class ApplyForm(nextcord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Apply for the Guild!", timeout=None)
        self.application_channel: nextcord.TextChannel = 945770316796403753

        self.ign = nextcord.ui.TextInput(
            label = "What is your ign?",
            placeholder="Ex: FirestarAD",
            style=nextcord.TextInputStyle.short,
            min_length=1,
        )

        self.add_item(self.ign)

        self.star = nextcord.ui.TextInput(
            label = "What star are you?",
            placeholder="Ex: 124",
            style=nextcord.TextInputStyle.short,
            min_length=1,
        )

        self.add_item(self.star)

        self.starsPerWeek = nextcord.ui.TextInput(
            label = "How many stars per week?",
            placeholder="Ex: 3 per week",
            style=nextcord.TextInputStyle.short,
            min_length=1,
        )

        self.add_item(self.starsPerWeek)

        self.friends = nextcord.ui.TextInput(
            label = "Do you know anyone in the guild?",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Ex: RYgamer1, FirestarAD, vxrco",
            min_length=1
        )

        self.add_item(self.friends)
    
        self.anything = nextcord.ui.TextInput(
            label = "Anything else you want us to know?",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Answer here :)"
        )

        self.add_item(self.anything)

    async def callback(self, ctx: nextcord.Interaction):
        await ctx.response.send_message("Complete!", ephemeral=True)

        channel: GuildChannel = ctx.guild.get_channel(self.application_channel)
                
        embed = nextcord.Embed(title=f"{ctx.user.name}'s Application")
        embed.add_field(name=self.ign.label, value=self.ign.value, inline=False)
        embed.add_field(name=self.star.label, value=self.star.value, inline=False)
        embed.add_field(name=self.starsPerWeek.label, value=self.starsPerWeek.value, inline=False)
        embed.add_field(name=self.friends.label, value=self.friends.value, inline=False)
        embed.add_field(name=self.anything.label, value=self.anything.value, inline=False)

        await channel.send(embed=embed)



def setup(client):
    client.add_cog(Settings(client))
