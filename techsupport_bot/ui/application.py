"""This is the ui object for the popup application form"""

from __future__ import annotations

import traceback
from typing import Self

import discord


class Application(discord.ui.Modal, title="Staff interest form"):
    """The class contianing the modal and all variables for it
    This must be sent as a response to an interaction, cannot be from a prefix command
    """

    background = discord.ui.TextInput(
        label="Do you have any IT or programming experience?",
        style=discord.TextStyle.long,
        required=True,
        max_length=300,
    )

    reason = discord.ui.TextInput(
        label="Why do you want to help here?",
        style=discord.TextStyle.long,
        required=True,
        max_length=300,
    )

    async def on_submit(self: Self, interaction: discord.Interaction) -> None:
        """What happens when the form has been successfully submitted

        Args:
            interaction (discord.Interaction): The interaction that caused the form to be show
        """
        await interaction.response.defer()
        return

    async def on_error(
        self: Self, interaction: discord.Interaction, error: Exception
    ) -> None:
        """What happens if there is an error in the application processing

        Args:
            interaction (discord.Interaction): The interaction that caused the form to be show
            error (Exception): The error generated by the application
        """
        await interaction.response.send_message(
            "Oops! Something went wrong. Try again or tell the server moderators if"
            " this keeps happening.",
            ephemeral=True,
        )

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
