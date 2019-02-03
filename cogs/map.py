from random import randint, choices, choice
from collections import Counter
from discord.ext import commands
from typing import Union
from io import BytesIO

import yaml

from .utils.data import Map, AdvancedMap
from .utils import checks
from .utils.translation import _


class Mapping:
    def __init__(self, bot):
        """Server map utilities"""
        self.bot = bot

    def generate_map(self, *, xsize: int, ysize: int, randoms: list):
        if xsize > 64 or ysize > 64 or xsize < 2 or ysize < 2:
            raise ValueError("x or y cannot exceed 64 and must be at least 2!")
        n = len(randoms) - 1
        mapping = ["".join(str(randint(0, n)) for _ in range(xsize)) for _ in range(ysize)]
        return mapping

    def create_map(self, xsize, ysize, generators, spawners):
        return Map(self.generate_map(xsize=xsize, ysize=ysize, randoms=generators), generators, spawners,
                   [xsize // 2, ysize // 2], xsize, ysize)

    @commands.group(invoke_without_command=True, aliases=["carte"])
    @checks.no_pm()
    async def map(self, ctx, name: str):
        """See the server map"""
        #
        # map = await self.bot.di.get_map(ctx.guild, name)
        # if map is None:
        #    await ctx.send("This server has no map of that name!")
        #    return

        # await ctx.send(f"{map.tiles}\n" + "\n".join(f"{i}: {item}" for i, item in enumerate(map.generators)))

    # Character meta has a "maps" key possibly, that will contain co-ords
    # "maps": {"Default": (0,0), "Moon": (32, 16)}

    @map.command()
    @checks.no_pm()
    async def create(self, ctx, mapname: str, xmax: int, ymax: int):
        """Create a map that will generate as it is explored. Set xmax and ymax to -1 for an infinite map
        ($5 Patrons only)
        """
        if xmax < 2 and xmax != -1:
            await ctx.send(await _(ctx, "xmax must be at least 2 or be -1!"))
            return

        if ymax < 2 and ymax != -1:
            await ctx.send(await _(ctx, "ymax must be at least 2 or be -1!"))
            return

        level = self.bot.patrons.get(ctx.guild.id, 0)

        if xmax > 64 or ymax > 256:
            if level == 0:
                await ctx.send(await _(ctx, "Only Patrons may make maps larger than 64x64 tiles!"))
                return
            elif level > 0:
                if xmax > 256 or ymax > 256:
                    if level > 5:
                        if xmax > 512 or ymax > 512:
                            await ctx.send(
                                await _(ctx, "You may not make maps greater than 512x512 unless they are infinite!"))
                            return
                    else:
                        await ctx.send(await _(ctx, "Only higher tier Patrons may make maps greater than 256x256"))
                        return

        maps = await self.bot.di.get_maps(ctx.guild)
        if -1 in (xmax, ymax):
            if level < 10:
                await ctx.send(await _(ctx,
                                       "Infinite maps are reserved for certain Patrons! See https://www.patreon.com/henry232323"
                                       ))
                return
            else:
                ninfmaps = sum(1 for mapi in maps.values() if -1 in (mapi.maxx, mapi.maxy))
                if ninfmaps >= 1:
                    if level < 15:
                        await ctx.send(await _(ctx,
                                               "You can only make one Infinite Map at this Patron level! Upgrade to make a second"
                                               ))
                        return
                    elif ninfmaps >= 2:
                        await ctx.send(await _(ctx,
                                               "You cannot make more than 2 infinite maps! (Ask Henry if you really want it)"))

        if len(maps) >= 3:
            level = self.bot.patrons.get(ctx.guild.id, 0)
            if len(maps) >= 5:
                if len(maps) >= 10:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 10 maps as of now! (Ask Henry if you really want it)"))
                    return
                elif level < 5:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 5 maps unless you are a higher level Patron!"))
                    return
            elif level < 1:
                await ctx.send(
                    await _(ctx, "Only Patrons may make more than 3 maps! See https://www.patreon.com/henry232323"))
                return

            await ctx.send(await _(ctx, "You can not have more than 3 maps unless you are a Patron! (For now)"))
            return

        await ctx.send(await _(ctx,
                               "What available tiles will there be? Say `done` when done. Use the * tile to describe all tiles "
                               "when adding what will spawn. One at a time send the name of the tile. i.e. grassland"))

        generators = []
        spawners = {}

        check = lambda x: x.channel.id == ctx.channel.id and x.author.id == ctx.author.id
        while True:
            await ctx.send(await _(ctx, "What kind of tile is it? Say `done` when done"))
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            tile = msg.content.strip()
            if tile == "done":
                break
            elif tile != "*":
                generators.append(tile)
            await ctx.send(await _(ctx,
                                   "What things might spawn in those tiles? Split terms with commas. (Equal chance of each, repeat a term "
                                   "for greater chance) `skip` to skip"
                                   ))
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content.lower() == "skip":
                continue
            spawners[(len(generators) - 1) if tile != "*" else -1] = Counter(x.strip() for x in msg.content.split(","))

        stile = [str(randint(0, len(generators) - 1))]
        new_map = Map(stile, generators, spawners, [0, 0], xmax, ymax)
        await self.bot.di.set_map(ctx.guild, mapname, new_map)
        await ctx.send((await _(ctx, "Map created with name {}")).format(mapname))

    @checks.admin_or_permissions()
    @map.command(aliases=["creer", "new", "nouvelle"])
    @checks.no_pm()
    async def generate(self, ctx, name: str, xsize: int, ysize: int):
        """Create a custom map for the guild.
        Usage: `rp!map create Earth 64 64`
            This will create a 64x64 map that will generate as the players explore it"""

        level = self.bot.patrons.get(ctx.guild.id, 0)
        if xsize < 2 and xsize != -1:
            await ctx.send(await _(ctx, "xsize must be at least 2!"))
            return

        if ysize < 2 and ysize != -1:
            await ctx.send(await _(ctx, "ysize must be at least 2!"))
            return

        if xsize > 64 or ysize > 64:
            if level == 0:
                await ctx.send(await _(ctx, "Only Patrons may make maps larger than 64x64 tiles!"))
                return
            elif level > 0:
                if xsize > 256 or ysize > 256:
                    if level > 5:
                        if xsize > 512 or ysize > 512:
                            await ctx.send(
                                await _(ctx, "You may not make maps greater than 512x512 unless they are infinite!"))
                            return
                    else:
                        await ctx.send(await _(ctx, "Only higher tier Patrons may make maps greater than 256x256"))
                        return

        maps = await self.bot.di.get_maps(ctx.guild)
        if len(maps) >= 3:
            if len(maps) >= 5:
                if len(maps) >= 10:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 10 maps as of now! (Ask Henry if you really want it)"))
                    return
                elif level < 5:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 5 maps unless you are a higher level Patron!"))
                    return
            elif level < 1:
                await ctx.send(
                    await _(ctx, "Only Patrons may make more than 3 maps! See https://www.patreon.com/henry232323"))
                return

        await ctx.send(await _(ctx,
                               "What available tiles will there be? Say `done` when done. Use the * tile to describe all tiles "
                               "when adding what will spawn. One at a time send the name of the tile. i.e. grassland"))

        generators = []
        spawners = {}

        check = lambda x: x.channel.id == ctx.channel.id and x.author.id == ctx.author.id
        while True:
            await ctx.send(await _(ctx, "What kind of tile is it? Say `done` when done"))
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            tile = msg.content.strip()
            if tile == "done":
                break
            elif tile != "*":
                generators.append(tile)
            await ctx.send(await _(ctx,
                                   "What things might spawn in those tiles? Split terms with commas. (Equal chance of each, repeat a term "
                                   "for greater chance) `skip` to skip"
                                   ))
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content.lower() == "skip":
                continue
            spawners[(len(generators) - 1) if tile != "*" else -1] = Counter(x.strip() for x in msg.content.split(","))

        new_map = self.create_map(xsize, ysize, generators, spawners)
        await self.bot.di.set_map(ctx.guild, name, new_map)
        await ctx.send(await _(ctx, "Map created!"))

    @map.command(aliases=["supprimer"])
    @checks.no_pm()
    @checks.admin_or_permissions()
    async def delete(self, ctx, *, name: str):
        """Delete a map"""
        await self.bot.di.remove_map(ctx.guild, name)
        await ctx.send((await _(ctx, "Map {} successfully deleted.")).format(name))

    @map.command(aliases=["north", "nord"])
    @checks.no_pm()
    async def up(self, ctx, mapname, character):
        """Move North on a map"""
        mapo = await self.bot.di.get_map(ctx.guild, mapname)
        char = await self.bot.di.get_character(ctx.guild, character)
        if char is None:
            await ctx.send(await _(ctx, "That character doesn't exist!"))
            return
        if char.owner != ctx.author.id:
            await ctx.send(await _(ctx, "You do not own this character!"))
            return
        if mapo is None:
            await ctx.send(await _(ctx, "This map does not exist!"))
            return

        spawn = mapo.spawn
        if not char.meta.get("maps"):
            char.meta["maps"] = {}
        if not char.meta["maps"].get(mapname):
            char.meta["maps"][mapname] = [0, 0]
        pos = char.meta["maps"][mapname]
        y = spawn[1] + pos[1]
        x = spawn[0] + pos[0]

        change = False
        lx = (len(mapo.tiles[0]) - 1)
        if x > lx:
            x = lx
            pos[0] = lx - spawn[0]
        elif x < 0:
            x = 0
            pos[0] = -spawn[0]

        ly = (len(mapo.tiles) - 1)
        if y > ly:
            y = ly
            pos[1] = ly - spawn[1]
        if y < 0:
            y = 0
            pos[1] = -spawn[1]

        if y == 0:
            if isinstance(mapo, AdvancedMap) or len(mapo.tiles) >= mapo.maxy and not mapo.maxy == -1:
                await ctx.send(await _(ctx, "You can't move any further this direction, you've hit the border!"))
                return
            else:
                change = True
                spawn[1] += 1
                fh = "?" * x + self.rtile(mapo)
                lh = "?" * (len(mapo.tiles[0]) - len(fh) - 1)
                mapo.tiles.insert(0, fh + lh)

        pos[1] -= 1
        changed, spawned, tile = self.explore(mapo, x, y)
        if tile == " ":
            await ctx.send(await _(ctx, "You cannot move any further in this direction!"))
            return
        if changed or change:
            await self.bot.di.set_map(ctx.guild, mapname, mapo)
        await self.bot.di.add_character(ctx.guild, char)

        if isinstance(mapo.generators, list):
            tstring = mapo.generators[int(tile)]
            if tstring is None:
                tstring = mapo.generators[tile]
        else:
            tstring = mapo.generators.get(int(tile))
            if tstring is None:
                tstring = mapo.generators.get(tile)
        await ctx.send((await _(ctx, "You enter a {}. You see {}")).format(tstring, spawned))

    @map.command(aliases=["south", "sud"])
    @checks.no_pm()
    async def down(self, ctx, mapname: str, character: str):
        """Move south on a map"""
        mapo = await self.bot.di.get_map(ctx.guild, mapname)
        char = await self.bot.di.get_character(ctx.guild, character)
        if char is None:
            await ctx.send(await _(ctx, "That character doesn't exist!"))
            return
        if char.owner != ctx.author.id:
            await ctx.send(await _(ctx, "You do not own this character!"))
            return
        if mapo is None:
            await ctx.send(await _(ctx, "This map does not exist!"))
            return

        spawn = mapo.spawn
        if not char.meta.get("maps"):
            char.meta["maps"] = {}
        if not char.meta["maps"].get(mapname):
            char.meta["maps"][mapname] = [0, 0]
        pos = char.meta["maps"][mapname]
        y = spawn[1] + pos[1]
        x = spawn[0] + pos[0]

        change = False
        lx = (len(mapo.tiles[0]) - 1)
        if x > lx:
            x = lx
            pos[0] = lx - spawn[0]
        elif x < 0:
            x = 0
            pos[0] = -spawn[0]

        ly = (len(mapo.tiles) - 1)
        if y > ly:
            y = ly
            pos[1] = ly - spawn[1]
        if y < 0:
            y = 0
            pos[1] = -spawn[1]

        if y == ly:
            if isinstance(mapo, AdvancedMap) or (ly + 1) >= mapo.maxy and not mapo.maxy == -1:
                await ctx.send(await _(ctx, "You can't move any further this direction, you've hit the border!"))
                return
            else:
                change = True
                fh = "?" * (x - 1) + self.rtile(mapo)
                lh = "?" * (len(mapo.tiles[0]) - len(fh))
                mapo.tiles.append(fh + lh)

        pos[1] += 1
        changed, spawned, tile = self.explore(mapo, x, y)
        if tile == " ":
            await ctx.send(await _(ctx, "You cannot move any further in this direction!"))
            return
        if changed or change:
            await self.bot.di.set_map(ctx.guild, mapname, mapo)
        await self.bot.di.add_character(ctx.guild, char)

        if isinstance(mapo.generators, list):
            tstring = mapo.generators[int(tile)]
            if tstring is None:
                tstring = mapo.generators[tile]
        else:
            tstring = mapo.generators.get(int(tile))
            if tstring is None:
                tstring = mapo.generators.get(tile)
        await ctx.send((await _(ctx, "You enter a {}. You see {}")).format(tstring, spawned))

    @map.command(aliases=["west", "ouest", "gauche"])
    @checks.no_pm()
    async def left(self, ctx, mapname: str, character: str):
        """Move West on a map"""
        mapo = await self.bot.di.get_map(ctx.guild, mapname)
        char = await self.bot.di.get_character(ctx.guild, character)
        if char is None:
            await ctx.send(await _(ctx, "That character doesn't exist!"))
            return
        if char.owner != ctx.author.id:
            await ctx.send(await _(ctx, "You do not own this character!"))
            return
        if mapo is None:
            await ctx.send(await _(ctx, "This map does not exist!"))
            return

        spawn = mapo.spawn
        if not char.meta.get("maps"):
            char.meta["maps"] = {}
        if not char.meta["maps"].get(mapname):
            char.meta["maps"][mapname] = [0, 0]
        pos = char.meta["maps"][mapname]
        y = spawn[1] + pos[1]
        x = spawn[0] + pos[0]

        change = False
        lx = (len(mapo.tiles[0]) - 1)
        if x > lx:
            x = lx
            pos[0] = lx - spawn[0]
        elif x < 0:
            x = 0
            pos[0] = -spawn[0]

        ly = (len(mapo.tiles) - 1)
        if y > ly:
            y = ly
            pos[1] = ly - spawn[1]
        if y < 0:
            y = 0
            pos[1] = -spawn[1]

        if x == 0:
            if isinstance(mapo, AdvancedMap) or len(mapo.tiles[0]) >= mapo.maxx and not mapo.maxx == -1:
                await ctx.send(await _(ctx, "You can't move any further this direction, you've hit the border!"))
                return
            else:
                change = True
                spawn[0] += 1
                for i in range(len(mapo.tiles)):
                    if i == y:
                        mapo.tiles[i] = self.rtile(mapo) + mapo.tiles[i]
                    else:
                        mapo.tiles[i] = "?" + mapo.tiles[i]

        pos[0] -= 1
        changed, spawned, tile = self.explore(mapo, x, y)
        if tile == " ":
            await ctx.send(await _(ctx, "You cannot move any further in this direction!"))
            return
        if changed or change:
            await self.bot.di.set_map(ctx.guild, mapname, mapo)
        await self.bot.di.add_character(ctx.guild, char)

        if isinstance(mapo.generators, list):
            tstring = mapo.generators[int(tile)]
            if tstring is None:
                tstring = mapo.generators[tile]
        else:
            tstring = mapo.generators.get(int(tile))
            if tstring is None:
                tstring = mapo.generators.get(tile)
        await ctx.send((await _(ctx, "You enter a {}. You see {}")).format(tstring, spawned))

    @map.command(aliases=["east", "est", "droit"])
    @checks.no_pm()
    async def right(self, ctx, mapname: str, character: str):
        """Move East on a map"""
        mapo = await self.bot.di.get_map(ctx.guild, mapname)
        char = await self.bot.di.get_character(ctx.guild, character)
        if char is None:
            await ctx.send(await _(ctx, "That character doesn't exist!"))
            return
        if char.owner != ctx.author.id:
            await ctx.send(await _(ctx, "You do not own this character!"))
            return
        if mapo is None:
            await ctx.send(await _(ctx, "This map does not exist!"))
            return

        spawn = mapo.spawn
        if not char.meta.get("maps"):
            char.meta["maps"] = {}
        if not char.meta["maps"].get(mapname):
            char.meta["maps"][mapname] = [0, 0]
        pos = char.meta["maps"][mapname]
        y = spawn[1] + pos[1]
        x = spawn[0] + pos[0]

        change = False

        lx = (len(mapo.tiles[0]) - 1)
        if x > lx:
            x = lx
            pos[0] = lx - spawn[0]
        elif x < 0:
            x = 0
            pos[0] = -spawn[0]

        ly = (len(mapo.tiles) - 1)
        if y > ly:
            y = ly
            pos[1] = ly - spawn[1]
        if y < 0:
            y = 0
            pos[1] = -spawn[1]

        if x == lx:
            if isinstance(mapo, AdvancedMap) or lx + 1 >= mapo.maxx and not mapo.maxy == -1:
                await ctx.send(await _(ctx, "You can't move any further this direction, you've hit the border!"))
                return
            else:
                change = True
                for i in range(len(mapo.tiles)):
                    if i == y:
                        mapo.tiles[i] += self.rtile(mapo)
                    else:
                        mapo.tiles[i] += "?"

        pos[0] += 1
        changed, spawned, tile = self.explore(mapo, x, y)
        if tile == " ":
            await ctx.send(await _(ctx, "You cannot move any further in this direction!"))
            return
        if changed or change:
            await self.bot.di.set_map(ctx.guild, mapname, mapo)
        await self.bot.di.add_character(ctx.guild, char)

        if isinstance(mapo.generators, list):
            tstring = mapo.generators[int(tile)]
            if tstring is None:
                tstring = mapo.generators[tile]
        else:
            tstring = mapo.generators.get(int(tile))
            if tstring is None:
                tstring = mapo.generators.get(tile)
        await ctx.send((await _(ctx, "You enter a {}. You see {}")).format(tstring, spawned))

        if isinstance(mapo, AdvancedMap):
            if spawned in mapo.spawnables:
                sp = mapo.spawnables[spawned]
                if "say" in sp:
                    await ctx.send(choice(sp["say"]).replace("{player}", str(ctx.author)))
                if "give" in sp:
                    await self.bot.di.give_items(ctx.author, *sp["give"])
                    await ctx.send((await _(ctx, "You acquired {}")).format(
                        ", ".join(f"{it}x{ni}" for it, ni in sp["give"].items())))
                if "shop" in sp:
                    await ctx.send((await _(ctx,
                                            "This tile has a shop that sells: {}")).format(
                        f"\n{it}: {ni}" for it, ni in sp["shop"].items()))

    @map.command()
    @checks.no_pm()
    async def buy(self, ctx, mapname: str, character: str, amount: int, itemname: str):
        """Buy an item from the shop on the current tile"""
        mapo = await self.bot.di.get_map(ctx.guild, mapname)
        char = await self.bot.di.get_character(ctx.guild, character)
        if char is None:
            await ctx.send(await _(ctx, "That character doesn't exist!"))
            return
        if char.owner != ctx.author.id:
            await ctx.send(await _(ctx, "You do not own this character!"))
            return
        if mapo is None:
            await ctx.send(await _(ctx, "This map does not exist!"))
            return

        if not isinstance(mapo, AdvancedMap):
            await ctx.send(await _(ctx, "There is no shop on this tile! (This map does not support shops!)"))

        spawn = mapo.spawn
        if not char.meta.get("maps"):
            char.meta["maps"] = {}
        if not char.meta["maps"].get(mapname):
            char.meta["maps"][mapname] = [0, 0]
        pos = char.meta["maps"][mapname]
        y = spawn[1] + pos[1]
        x = spawn[0] + pos[0]

        __, spawned, tile, = self.explore(mapo, x, y)
        sp = mapo.spawnables.get(spawned)
        if sp and "shop" in sp:
            try:
                await self.bot.di.add_eco(ctx.author, -sp[itemname] * amount)
                await self.bot.di.give_items(ctx.author, (itemname, amount))
                await ctx.send((await _(ctx, "Successfully bought {} {}s")).format(amount, itemname))
            except ValueError:
                await ctx.send(await _(ctx, "You can't afford this many!"))
            except KeyError:
                await ctx.send(await _(ctx, "This shop sells no such item!"))
        else:
            await ctx.send(await _(ctx, "There is no shop here!"))

    def explore(self, mapo: Union[Map, AdvancedMap], x: int, y: int):
        tile = mapo.tiles[y][x]
        changed = False
        if tile == "?":
            changed = True
            f = list(mapo.tiles[y])
            f[x] = self.rtile(mapo)
            mapo.tiles[y] = "".join(f)
            tile = f[x]

        if not isinstance(mapo, AdvancedMap):
            spawnable = mapo.spawners.get(tile)
            if not spawnable:
                spawnable = mapo.spawners.get('-1')
            if not spawnable:
                spawned = "nothing"
            else:
                spawned = choices(*zip(*spawnable.items()))[0]
                if spawned is None:
                    spawned = "nothing"
        else:
            spawnable = mapo.spawners.get(mapo.generators[tile])
            if not spawnable:
                spawnable = mapo.spawners.get('*')
            if not spawnable:
                spawned = "nothing"
            else:
                spawned = choice(spawnable)
                if spawned is None:
                    spawned = "nothing"

        return changed, spawned, tile

    @map.command(aliases=["look", "regarder", "inspect", "voir"])
    @checks.no_pm()
    async def check(self, ctx, mapname: str, character: str):
        """Inspect the current tile a character is on"""
        try:
            mapo = await self.bot.di.get_map(ctx.guild, mapname)
            char = await self.bot.di.get_character(ctx.guild, character)
            if char is None:
                await ctx.send(await _(ctx, "That character doesn't exist!"))
                return
            if char.owner != ctx.author.id:
                await ctx.send(await _(ctx, "You do not own this character!"))
                return
            if mapo is None:
                await ctx.send(await _(ctx, "This map does not exist!"))
                return

            spawn = mapo.spawn
            if not char.meta.get("maps"):
                char.meta["maps"] = {}
            if not char.meta["maps"].get(mapname):
                char.meta["maps"][mapname] = [0, 0]
            pos = char.meta["maps"][mapname]
            y = spawn[1] + pos[1]
            x = spawn[0] + pos[0]

            if isinstance(mapo, AdvancedMap):
                surrounding = self.ndslice(mapo.tiles, (max(y - 1, 0), max(y + 2, len(mapo.tiles))),
                                           (max(x - 1, 0), max(x + 2, len(mapo.tiles[0]))))
                await ctx.send("```{}```".format('\n'.join(surrounding)))
                await ctx.send("```{}```".format("\n".join(f"{i}: {item}" for i, item in mapo.generators.items())))
            else:
                surrounding = self.ndslice(mapo.tiles, (max(y - 1, 0), max(y + 2, mapo.maxy)),
                                           (max(x - 1, 0), max(x + 2, mapo.maxx)))
                await ctx.send("```{}```".format('\n'.join(surrounding)))
                await ctx.send("```{}```".format("\n".join(f"{i}: {item}" for i, item in enumerate(mapo.generators))))
        except:
            from traceback import print_exc
            print_exc()

    @staticmethod
    def rtile(mapo):
        return str(randint(0, len(mapo.generators) - 1))

    @staticmethod
    def ndslice(l, ysl, xsl):
        return [e[slice(*ysl)] for e in l[slice(*xsl)]]

    @map.command(aliases=["upload"])
    @checks.no_pm()
    @checks.admin_or_permissions()
    async def load(self, ctx, name: str):
        if not ctx.message.attachments:
            await ctx.send(await _(ctx, "This command needs to have a file attached!"))
            return

        attachment = ctx.message.attachments.pop()
        size = attachment.size
        if size > 2 ** 20:
            await ctx.send(await _(ctx, "This file is too large!"))
            return

        file = BytesIO()
        await attachment.save(file)
        file.seek(0)
        mapspace, mapdata = self.parsemap(file)
        xsize, ysize = len(mapspace[0]), len(mapspace)
        level = self.bot.patrons.get(ctx.guild.id, 0)

        if xsize > 64 or ysize > 64:
            if level == 0:
                await ctx.send(await _(ctx, "Only Patrons may make maps larger than 64x64 tiles!"))
                return
            elif level > 0:
                if xsize > 256 or ysize > 256:
                    if level > 5:
                        if xsize > 512 or ysize > 512:
                            await ctx.send(
                                await _(ctx, "You may not make maps greater than 512x512 unless they are infinite!"))
                            return
                    else:
                        await ctx.send(await _(ctx, "Only higher tier Patrons may make maps greater than 256x256"))
                        return

        maps = await self.bot.di.get_maps(ctx.guild)
        if len(maps) >= 3:
            if len(maps) >= 5:
                if len(maps) >= 10:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 10 maps as of now! (Ask Henry if you really want it)"))
                    return
                elif level < 5:
                    await ctx.send(
                        await _(ctx, "You cannot make more than 5 maps unless you are a higher level Patron!"))
                    return
            elif level < 1:
                await ctx.send(
                    await _(ctx, "Only Patrons may make more than 3 maps! See https://www.patreon.com/henry232323"))
                return

        fullmap = AdvancedMap(mapspace, mapdata["generators"], mapdata["spawners"], mapdata["spawnables"],
                              mapdata.get("spawn", (0, 0)), True)
        await self.bot.di.set_map(ctx.guild, name, fullmap)
        await ctx.send((await _(ctx, "Map created with name {}")).format(name))

    @staticmethod
    def parsemap(file):
        mapspace = []
        last, current = "", file.readline().decode()
        while (last.strip(), current.strip()) != ("", ""):
            if current.strip():
                mapspace.append(current.strip("\r").strip("\n"))
            last, current = current, file.readline().decode()

        maxlen = len(max(mapspace, key=lambda x: len(x)))
        for i, line in enumerate(mapspace):
            linelen = len(line)
            if linelen < maxlen:
                mapspace[i] += " " * (maxlen - linelen)  # pad lines with spaces

        return mapspace, yaml.safe_load(file)
