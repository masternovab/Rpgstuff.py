from discord.ext import commands
import discord

from .utils import checks, data
from .utils.data import chain
from .utils.translation import _


class User(object):
    """Commands for guild management"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["ui"])
    @checks.no_pm()
    async def ui(self, ctx, *, user: discord.Member = None):
        """Get info on a user"""
        if user is None:
            user = ctx.author

        embed = discord.Embed()
        embed.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        ud = await self.bot.db.get_user_data(user)
        gd = await self.bot.db.get_guild_data(ctx.guild)

        pokemon = [f"{x[0]}: **{x[1]}**" for x in ud["box"]]
        pl = len(pokemon)
        if pl > 20:
            pokemon = pokemon[20:]
            pokemon.append((await _(ctx, "\nand {} more...")).format(pl - 20))
        boxitems = "\n".join(pokemon)

        imap = [f"{x[0]} x{x[1]}" for x in ud["items"].items()]
        il = len(imap)
        if il > 20:
            imap = imap[:20]
            imap.append((await _(ctx, "\nand {} more...")).format(il - 20))
        invitems = "\n".join(imap) or await _(ctx, "No Items")

        embed.add_field(name=await _(ctx, "Balance"), value=f"{ud['money']} {gd.get('currency', 'dollars')}")
        embed.add_field(name=await _(ctx, "Guild"), value=ud.get("guild", await _(ctx, "None")))
        embed.add_field(name=await _(ctx, "Items"), value=invitems)
        embed.add_field(name=await _(ctx, "Box"), value=boxitems) if boxitems else None
        embed.add_field(name=await _(ctx, "Experience"),
                        value=(await _(ctx, "Level: {}\nExperience: {}/{}")).format(ud.get('level', 1),
                                                                                    ud.get('exp', 0),
                                                                                    self.bot.get_exp(
                                                                                        ud.get('level', 1))))

        await ctx.send(embed=embed)

    @checks.no_pm()
    @checks.mod_or_permissions()
    @commands.group(aliases=["exp"], invoke_without_command=True)
    async def experience(self, ctx, member: discord.Member = None):
        """Get your or another user's level information. Help on this command for experience subcommands
        EXP is calculated using a 0.1x^2+5x+4 where x is equal to the user's current level
        Spamming commands or messages will not earn more exp!"""
        if member is None:
            member = ctx.author

        ulvl, uexp = await self.bot.di.get_user_level(member)
        embed = discord.Embed(
            description=(await _(ctx, "Level: {}\nExperience: {}/{}")).format(ulvl, uexp, self.bot.get_exp(ulvl)))
        embed.set_author(name=member.display_name, icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @checks.no_pm()
    @checks.mod_or_permissions()
    @experience.command(aliases=["set"])
    async def setlevel(self, ctx, level: data.IntConverter, *members: data.MemberConverter):
        """Set the given members level"""
        members = chain(members)
        for member in members:
            await self.bot.di.set_level(member, level, 0)
        await ctx.send(await _(ctx, "Set level for members"))

    @checks.no_pm()
    @checks.mod_or_inv()
    @experience.command()
    async def add(self, ctx, amount: data.IntConverter, *members: data.MemberConverter):
        """Give the given members an amount of experience"""
        members = chain(members)
        for member in members:
            await self.bot.di.add_exp(member, amount)

        await ctx.send(await _(ctx, "Gave experience to members"))

    @checks.no_pm()
    @experience.command()
    @checks.mod_or_permissions()
    async def enable(self, ctx):
        """Enable EXP settings for a guild"""
        await self.bot.di.set_exp_enabled(ctx.guild, True)
        await ctx.send(await _(ctx, "Successfully changed EXP setting"))

    @checks.no_pm()
    @experience.command()
    @checks.mod_or_permissions()
    async def disable(self, ctx):
        """Disable EXP settings for a guild"""
        await self.bot.di.set_exp_enabled(ctx.guild, False)
        await ctx.send(await _(ctx, "Successfully changed EXP setting"))
