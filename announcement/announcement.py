import discord
import typing
import re
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class AnnoucementPlugin(commands.Cog):
    """
    Easily create plain text or embedded announcements
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.group(aliases=["a"], invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def announcement(self, ctx: commands.Context):
        """
        Make Announcements Easily
        """
        await ctx.send_help(ctx.command)
   
    @announcement.command()
    @checks.has_permissions(PermissionLevel.ADMIN)
    async def quick(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel,
        role: typing.Optional[typing.Union[discord.Role, str]],
        *,
        msg: str,
    ):
        """
        An old way of making announcements

        **Usage:**
        {prefix}announcement quick #channel <OPTIONAL role> message
        """
        if isinstance(role, discord.Role):
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            await grole.edit(mentionable=True)

        await channel.send(f"{659115529100853306}\n{msg}")
        await ctx.send("Done")

        if isinstance(role, discord.Role):
            guild: discord.Guild = ctx.guild
            grole: discord.Role = guild.get_role(role.id)
            if grole.mentionable is True:
                await grole.edit(mentionable=False)

    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.session.post(
            "https://counter.modmail-plugins.piyush.codes/api/instances/announcement",
            json={"id": self.bot.user.id},
        ):
            print("Posted to Plugin API")


def setup(bot):
    bot.add_cog(AnnoucementPlugin(bot))
