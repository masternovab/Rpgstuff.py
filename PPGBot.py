import asyncio
import datetime
import logging
import os
import sys
import ujson as json
from collections import Counter
from random import choice, sample

import aiohttp
import discord
import psutil
from datadog import ThreadStats
from datadog import initialize as init_dd
from discord.ext import commands

from pyhtml import server
import cogs
from cogs.utils import db, data
from cogs.utils.translation import _

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    uvloop = None

if os.name == "nt":
    sys.argv.append("debug")
elif os.getcwd().endswith("rpgtest"):
    sys.argv.append("debug")


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, shard_count=5, game=discord.Game(name="rp!help for help!"), **kwargs)
        self.owner_id = 477463812786618388
        self.lounge_id = 530023045918883840
        self.uptime = datetime.datetime.utcnow()
        self.commands_used = Counter()
        self.server_commands = Counter()
        self.socket_stats = Counter()
        self.shutdowns = []
        self.lotteries = dict()

        self.logger = logging.getLogger('discord')  # Discord Logging
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename=os.path.join('resources', 'discord.log'), encoding='utf-8',
                                           mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

        self.session = aiohttp.ClientSession(loop=self.loop)
        self.shutdowns.append(self.shutdown)

        with open("resources/auth") as af:
            self._auth = json.loads(af.read())

        with open("resources/dnditems.json", 'r') as dndf:
            self.dnditems = json.loads(dndf.read())

        with open("resources/dnditems.json", 'r') as dndf2:
            self.dndmagic = json.loads(dndf2.read())

        with open("resources/pokemonitems.json", 'r') as dndf3:
            self.pokemonitems = json.loads(dndf3.read())

        self.httpserver = server.API(self, "RPGBot")
        server.makepaths(self.httpserver)

        self.db: db.Database = db.Database(self)
        self.di: data.DataInteraction = data.DataInteraction(self)
        self.default_udata = data.default_user
        self.default_servdata = data.default_server
        self.rnd = "1234567890abcdefghijklmnopqrstuvwxyz"

        with open("resources/patrons.json") as pj:
            self.patrons = {int(k): v for k, v in json.loads(pj.read()).items()}

        with open("resources/newtranslations.json") as trf:
            self.translations = json.loads(trf.read())
        self.languages = ["en", "fr", "de", "ru", "es"]

        with open("resources/blacklist.json") as blf:
            self.blacklist = json.loads(blf.read())

        icogs = [
            cogs.admin.Admin(self),
            cogs.team.Team(self),
            cogs.economy.Economy(self),
            cogs.inventory.Inventory(self),
            cogs.settings.Settings(self),
            cogs.misc.Misc(self),
            cogs.characters.Characters(self),
            cogs.pokemon.Pokemon(self),
            cogs.groups.Groups(self),
            cogs.user.User(self),
            cogs.salary.Salary(self),
            cogs.map.Mapping(self),
        ]
        for cog in icogs:
            self.add_cog(cog)

        # self.loop.create_task(self.start_serv())
        self.loop.create_task(self.httpserver.host())

        init_dd(self._auth[3], self._auth[4])
        self.stats = ThreadStats()
        self.stats.start()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.loop.create_task(self.update_stats())

    async def on_message(self, msg):
        if msg.author.id not in self.blacklist:
            ctx = await self.get_context(msg)
            await self.invoke(ctx)

    async def update_stats(self):
        url = "https://bots.discord.pw/api/bots/{}/stats".format(self.user.id)
        while not self.is_closed():
            payload = json.dumps(dict(server_count=len(self.guilds))).encode()
            headers = {'authorization': self._auth[1], "Content-Type": "application/json"}

            async with self.session.post(url, data=payload, headers=headers) as response:
                await response.read()

            url = "https://discordbots.org/api/bots/{}/stats".format(self.user.id)
            payload = json.dumps(dict(server_count=len(self.guilds))).encode()
            headers = {'authorization': self._auth[2], "Content-Type": "application/json"}

            async with self.session.post(url, data=payload, headers=headers) as response:
                await response.read()

            await asyncio.sleep(14400)

    async def on_command(self, ctx):
        self.stats.increment("RPGBot.commands", tags=["RPGBot:commands"], host="scw-8112e8")
        self.stats.increment(f"RPGBot.commands.{str(ctx.command).replace(' ', '.')}", tags=["RPGBot:commands"],
                             host="scw-8112e8")
        self.commands_used[ctx.command] += 1
        if isinstance(ctx.author, discord.Member):
            self.server_commands[ctx.guild.id] += 1
            if ctx.guild.id not in self.patrons:
                if (self.server_commands[ctx.guild.id] % 50) == 0:
                    await ctx.send(await _(ctx,
                                           "This bot costs $300/yr to run. If you like the utilities it provides,"
                                           " consider buying me a coffee <https://ko-fi.com/henrys>"
                                           " or subscribe as a Patron <https://www.patreon.com/henry232323>"
                                           " Also consider upvoting the bot to help us grow <https://discordbots.org/bot/305177429612298242>"
                                           ))

            if await self.di.get_exp_enabled(ctx.guild):
                add = choice([0, 0, 0, 0, 0, 1, 1, 2, 3])
                fpn = ctx.command.full_parent_name.lower()
                if fpn:
                    values = {
                        "character": 2,
                        "inventory": 1,
                        "economy": 1,
                        "pokemon": 2,
                        "guild": 2,
                        "team": 1,
                    }
                    add += values.get(fpn, 0)

                if add:
                    await asyncio.sleep(4)
                    r = await self.di.add_exp(ctx.author, add)
                    if r is not None:
                        await ctx.message.add_reaction("\u23EB")
            time = await self.di.get_delete_time(ctx.guild)
            if time:
                await asyncio.sleep(time)
                await ctx.message.delete()

    async def on_command_error(self, ctx, exception):
        self.stats.increment("RPGBot.errors", tags=["RPGBot:errors"], host="scw-8112e8")
        logging.info(f"Exception in {ctx.command} {ctx.guild}:{ctx.channel} {exception}")
        if isinstance(exception, commands.MissingRequiredArgument):
            await ctx.send(f"`{exception}`")
        elif isinstance(exception, TimeoutError):
            await ctx.send(await _(ctx, "This operation ran out of time! Please try again"))
        else:
            await ctx.send(f"`{exception}`")

    async def on_guild_join(self, guild):
        if guild.id in self.blacklist:
            await guild.leave()

        self.stats.increment("RPGBot.guilds", tags=["RPGBot:guilds"], host="scw-8112e8")

    async def on_guild_leave(self, guild):
        self.stats.increment("RPGBot.guilds", -1, tags=["RPGBot:guilds"], host="scw-8112e8")

    async def on_socket_response(self, msg):
        self.socket_stats[msg.get('t')] += 1

    async def get_bot_uptime(self):
        """Get time between now and when the bot went up"""
        now = datetime.datetime.utcnow()
        delta = now - self.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if days:
            fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h} hours, {m} minutes, and {s} seconds'

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    def randsample(self):
        return "".join(sample(self.rnd, 6))

    @staticmethod
    def get_exp(level):
        return int(0.1 * level ** 2 + 5 * level + 4)

    @staticmethod
    def get_ram():
        """Get the bot's RAM usage info."""
        mem = psutil.virtual_memory()
        return f"{mem.used / 0x40_000_000:.2f}/{mem.total / 0x40_000_000:.2f}GB ({mem.percent}%)"

    @staticmethod
    def format_table(lines, separate_head=True):
        """Prints a formatted table given a 2 dimensional array"""
        # Count the column width
        widths = []
        for line in lines:
            for i, size in enumerate([len(x) for x in line]):
                while i >= len(widths):
                    widths.append(0)
                if size > widths[i]:
                    widths[i] = size

        # Generate the format string to pad the columns
        print_string = ""
        for i, width in enumerate(widths):
            print_string += "{" + str(i) + ":" + str(width) + "} | "
        if not len(print_string):
            return
        print_string = print_string[:-3]

        # Print the actual data
        fin = []
        for i, line in enumerate(lines):
            fin.append(print_string.format(*line))
            if i == 0 and separate_head:
                fin.append("-" * (sum(widths) + 3 * (len(widths) - 1)))

        return "\n".join(fin)

    async def shutdown(self):
        self.session.close()


prefix = ['N!','<@520550412219318272>'] if "debug" not in sys.argv else 'rp$'
invlink = "https://discordapp.com/api/oauth2/authorize?client_id=520550412219318272&permissions=8&scope=bot"
servinv = "https://discord.gg/AbxYmAa"
sourcelink = "https://github.com/henry232323/RPGBot"
description = f"A Bot for assisting with RPG made by XxKingNovaXx#0416," \
              " with a working inventory, market and economy," \
              " team setups and characters as well. Each user has a server unique inventory and balance." \
              " Players may list items on a market for other users to buy." \
              " Users may create characters with teams from Pokemon in their storage box. " \
              "Server administrators may add and give items to the server and its users.```\n" \
              f"**Add to your server**: {invlink}\n" \
              f"**Support Server**: {servinv}\n" \
              f"**Source**: {sourcelink}\n" \
              "**Help**: https://github.com/henry232323/RPGBot/blob/master/README.md\n" \
              
             

with open("resources/auth") as af:
    _auth = json.loads(af.read())

prp = Bot(command_prefix=prefix, description=description, pm_help=True)
prp.run(_auth[0])
