import io
import os
import sys
import copy
import psutil
import asyncio
import discord
from textwrap import indent
from .utils import checks
from .utils.translation import _
from inspect import isawaitable
from discord.ext import commands
from traceback import format_exc
from contextlib import redirect_stdout


class Admin(object):
    def __init__(self, bot):
        self.emote = None
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code. Borrowed from RoboDanny"""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @checks.is_owner()
    @commands.command(hidden=True)
    async def eval(self, ctx, *, body: str):
        """Borrowed from RoboDanny"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.guild,
            'guild': ctx.message.guild,
            'message': ctx.message,
            '_': self._last_result,
            'self': self,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send('```py\n{}{}\n```'.format(value, format_exc()))
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send('```py\n%s\n```' % value)
            else:
                self._last_result = ret
                await ctx.send('```py\n%s%s\n```' % (value, ret))

    @commands.command(hidden=True)
    @checks.is_owner()
    async def repeatcommand(self, ctx, times: int, *, command):
        """Repeats a command a specified number of times."""
        msg = copy.copy(ctx.message)
        msg.content = command
        for i in range(times):
            await self.bot.process_commands(msg)

    @checks.no_pm()
    @commands.command(hidden=True)
    @checks.owner_or_permissions(manage_messagees=True)
    async def clear(self, ctx, number: int):
        """Purge messages"""
        if number > 100:
            await ctx.send(await _(ctx, "Cannot purge more than 100 messages!"))
            return

        await ctx.message.channel.purge(limit=number)

    @commands.command(hidden=True)
    @checks.is_owner()
    async def logout(self, ctx):
        await ctx.send("Logging out")
        self.bot.running = False
        for shutdown in self.bot.shutdowns:
            await shutdown()
        await self.bot.logout()
