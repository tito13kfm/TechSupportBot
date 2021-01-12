from cogs import HttpPlugin
from discord.ext import commands
from helper import with_typing


def setup(bot):
    bot.add_cog(Wolfram(bot))


class Wolfram(HttpPlugin):

    PLUGIN_NAME = __name__
    API_URL = "http://api.wolframalpha.com/v1/result?appid={}&i={}"

    @with_typing
    @commands.has_permissions(send_messages=True)
    @commands.command(
        name="wa",
        aliases=["math"],
        brief="Search Wolfram Alpha",
        description="Searches the simple answer Wolfram Alpha API",
        usage="[query]",
    )
    async def simple_search(self, ctx, *args):
        if not args:
            await self.bot.h.tagged_response(ctx, "Please provide a query!")
            return

        query = "+".join(args)

        url = self.API_URL.format(self.config.api_key, query)

        response = await self.http_call("get", url)

        if not response.text:
            await self.bot.h.tagged_response(ctx, "No results found")
            return

        await self.bot.h.tagged_response(ctx, response.text)
