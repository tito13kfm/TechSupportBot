"""Module for the Spotify extension of the discord bot."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

import aiohttp
import ui
from core import auxiliary, cogs
from discord.ext import commands

if TYPE_CHECKING:
    import bot


async def setup(bot: bot.TechSupportBot) -> None:
    """Loading the Spotify plugin into the bot

    Args:
        bot (bot.TechSupportBot): The bot object to register the cogs to

    Raises:
        AttributeError: Raised if an API key is missing to prevent unusable commands from loading
    """

    # Don't load without the API key
    try:
        if not bot.file_config.api.api_keys.spotify_client:
            raise AttributeError("Spotify was not loaded due to missing API key")
        if not bot.file_config.api.api_keys.spotify_key:
            raise AttributeError("Spotify was not loaded due to missing API key")
    except AttributeError as exc:
        raise AttributeError("Spotify was not loaded due to missing API key") from exc

    await bot.add_cog(Spotify(bot=bot))


class Spotify(cogs.BaseCog):
    """Class for setting up the Spotify extension."""

    AUTH_URL = "https://accounts.spotify.com/api/token"
    API_URL = "https://api.spotify.com/v1/search"

    async def get_oauth_token(self: Self) -> str:
        """Method to get an oauth token for the Spotify API."""
        data = {"grant_type": "client_credentials"}
        response = await self.bot.http_functions.http_call(
            "post",
            self.AUTH_URL,
            data=data,
            auth=aiohttp.BasicAuth(
                self.bot.file_config.api.api_keys.spotify_client,
                self.bot.file_config.api.api_keys.spotify_key,
            ),
        )

        return response.get("access_token")

    @auxiliary.with_typing
    @commands.command(
        brief="Searches Spotify",
        description="Returns Spotify track results",
        usage="[query]",
    )
    async def spotify(self: Self, ctx: commands.Context, *, query: str) -> None:
        """Method to return a song from the Spotify API."""
        oauth_token = await self.get_oauth_token()
        if not oauth_token:
            await auxiliary.send_deny_embed(
                message="I couldn't authenticate with Spotify", channel=ctx.channel
            )
            return

        headers = {"Authorization": f"Bearer {oauth_token}"}
        params = {"q": query, "type": "track", "market": "US", "limit": 3}
        response = await self.bot.http_functions.http_call(
            "get", self.API_URL, headers=headers, params=params
        )

        items = response.get("tracks", {}).get("items", [])

        if not items:
            await auxiliary.send_deny_embed(
                message="I couldn't find any results", channel=ctx.channel
            )
            return

        links = []
        for item in items:
            song_url = item.get("external_urls", {}).get("spotify")
            if not song_url:
                continue
            links.append(song_url)

        if not links:
            await auxiliary.send_deny_embed(
                message="I had trouble parsing the search results", channel=ctx.channel
            )
            return

        await ui.PaginateView().send(ctx.channel, ctx.author, links)
