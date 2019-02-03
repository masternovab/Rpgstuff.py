import ujson as json
import asyncpg
import copy


class Database(object):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def dump(data):
        return json.dumps(data).replace("'", "''")

    async def connect(self):
        self._conn = await asyncpg.create_pool(user='root', password='root',
                                  database='pokerpg', host='127.0.0.1')

    # User functions
    ########################################################################
    async def user_insert(self, member, data):
        """Create a new user entry with the given data"""
        jd = self.dump({member.guild.id: data})
        req = f"""INSERT INTO userdata (UUID, info) VALUES ({member.id}, '{jd}')"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
            return json.decode(response) if response else response

    async def user_select(self, member):
        """Select a user's data for a specified server"""
        req = f"""SELECT info -> '{member.guild.id}' FROM userdata WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def user_full_select(self, member):
        """Select a user's data for a specified server"""
        req = f"""SELECT info FROM userdata WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def user_update(self, member, data):
        """Update a user's data for a specific server"""
        jd = self.dump(data)
        req = f"""UPDATE userdata
        SET info = '{jd}'
        WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def user_exists(self, member):
        """Check if a user has an entry in the db"""
        req = f"""SELECT info FROM userdata WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            return bool(await connection.fetchval(req))

    async def add_user(self, member, data=None):
        """Add a server to the users json, if the user doesnt exist user_insert to make one"""
        if not data:
            data = {member.guild.id: self.bot.default_udata}

        if not await self.user_exists(member):
            await self.user_insert(member, data)
            return

        else:
            values = await self.user_select(member)

        if not values:
            await self.update_user_data(member, data)

    async def update_user_data(self, member, data):
        """Update a user's server data"""
        fs = await self.user_full_select(member)
        if fs:
            fs.update({str(member.guild.id): data})
            await self.user_update(member, fs)
        else:
            await self.user_insert(member, data)

    async def get_user_data(self, member):
        """Get a user's data for a server"""
        data = await self.user_select(member)
        return data if data else copy.copy(self.bot.default_udata)

    async def get_all_user_data(self, member):
        """Get a user's data for all servers"""
        req = f"""SELECT info FROM userdata WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    # Server functions
    ########################################################################
    async def guild_insert(self, guild, data):
        """Add a new guild to the db"""
        jd = self.dump(data)
        req = f"""INSERT INTO servdata (UUID, info) VALUES ({guild.id}, '{jd}')"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def guild_select(self, guild):
        """Get a guild from the db"""
        req = f"""SELECT info FROM servdata WHERE UUID = {guild.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def guild_update(self, guild, data):
        """Update a guild"""
        jd = self.dump(data)
        req = f"""UPDATE servdata
        SET info = '{jd}'
        WHERE UUID = {guild.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return json.decode(response) if response else response

    async def add_guild(self, guild, data=None):
        """Add a guild to the db"""
        values = await self.guild_select(guild)
        if values:
            return

        if not data:
            data = self.bot.default_servdata

        await self.guild_insert(guild, data)

    async def update_guild_data(self, guild, data):
        if await self.guild_select(guild):
            await self.guild_update(guild, data)
        else:
            await self.guild_insert(guild, data)

    async def get_guild_data(self, guild):
        values = await self.guild_select(guild)
        if values:
            return values
        else:
            await self.guild_insert(guild, self.bot.default_servdata)
            return await self.get_guild_data(guild)

    async def guild_item(self, guild, name: str):
        req = f"""SELECT info ->> '{name}' FROM servdata WHERE UUID = {guild.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return response if response else copy.copy(self.bot.default_servdata[name])

    async def user_item(self, member, name: str):
        req = f"""SELECT info -> '{member.guild.id}' ->> '{name}' FROM userdata WHERE UUID = {member.id}"""
        async with self._conn.acquire() as connection:
            response = await connection.fetchval(req)
        return response if response else copy.copy(self.bot.default_udata[name])
