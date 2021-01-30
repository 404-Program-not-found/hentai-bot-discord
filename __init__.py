from discord.ext import commands
import discord
import os
from enum import Enum
import json
import asyncio
import random

intents = discord.Intents.default()
intents.members = True

startup_extensions = ["Hentai"]


class Emoji(Enum):
    english = ":flag_gb:"
    chinese = ":flag_cn:"
    japanese = ":flag_jp:"
    korean = ":flag_kr:"
    spanish = ":flag_ea:"
    german = ":flag_de:"
    found = ":question:"

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@commands.is_owner()
@bot.command()
async def load(ctx, extension_name: str):
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@commands.is_owner()
@bot.command()
async def reload(ctx, extension_name: str):
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} reloaded.".format(extension_name))


async def checkready(times):
    for i in range(0, times):
        if not bot.is_ready():
            return False
        await asyncio.sleep(5)
    return True


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('{} Loaded! You are using the correct file'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(os.environ['discord_api_key'])
