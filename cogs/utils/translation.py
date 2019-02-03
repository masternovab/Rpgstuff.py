async def _(ctx, translation):
    if ctx.guild is not None:
        gd = await ctx.bot.db.get_guild_data(ctx.guild)
        lang = gd.get("lang", "en")
        currency = gd.get("currency", "dollars")
        if lang == "en":
            return translation.replace("dollars", currency)

        try:
            translation = ctx.bot.translations[translation][lang]
            return translation.replace("dollars", currency)
        except:
            return translation.replace("dollars", currency)

    return translation
