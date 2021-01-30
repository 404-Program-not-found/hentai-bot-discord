import discord
from discord.ext import commands
import re
import nhentai
from __init__ import Emoji


class Hentai(commands.Cog):
    def __init__(self, bot):
        pass
    def nuke_gui(self, code):
        dataset = nhentai.get_doujin(code)
        metadata = {"artist": "Not Found", "tags": "Not Found", "language": "found"}
        for x in dataset.__dict__["tags"]:
            if x[1] == "artist":
                metadata["artist"] = x[2]
            if x[1] == "tag":
                if metadata["tags"] == "Not Found":
                    metadata["tags"] = x[2]
                else:
                    metadata["tags"] = metadata["tags"] + f", {x[2]}"
            if x[1] == "language":
                if metadata["language"] == "found":
                    metadata["language"] = x[2]
        embedvar = discord.Embed(title=f"{Emoji[metadata['language']].value} {dataset.titles['pretty']}",
                                 description=dataset.url,
                                 colour=0x039e00)
        embedvar.set_image(url=dataset.thumbnail)
        embedvar.add_field(name="Author", value=metadata["artist"])
        embedvar.add_field(name="Favorites", value=dataset.favorites)
        embedvar.set_footer(text=f"Tags: {metadata['tags']}")
        return embedvar

    @commands.Cog.listener()
    async def on_message(self, message):
        launch_codes = re.findall(r"(\d{6})", message.content)
        if launch_codes and message.channel.nsfw:
            for nuke_codes in launch_codes:
                try:
                    embedvar = self.nuke_gui(nuke_codes)
                    await message.channel.send(embed=embedvar)
                except Exception as error:
                    print(error)

    @commands.command()
    @commands.is_nsfw()
    async def rollfap(self, ctx):
        await ctx.message.channel.send(embed=self.nuke_gui(nhentai.get_random_id()))




def setup(bot):
    bot.add_cog(Hentai(bot))
