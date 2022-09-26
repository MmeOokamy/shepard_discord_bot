import os
import discord
from discord.ext import commands

# Define a simple View that gives us a confirmation menu
from db import db_fight_get_adversary


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Oui', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Non', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


class AdvChoices(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.label = ""

    @discord.ui.button(label="Numero1", style=discord.ButtonStyle.grey)
    async def adv_one(self, interaction: discord.Interaction, button: discord.ui.Button, ctx: commands.Context):
        await interaction.response.send_message("Ton adversaire sera : 1")
        self.label = "adv['adv_name']"
        self.value = "adv['id']"

    @discord.ui.button(label="x", style=discord.ButtonStyle.danger)
    async def adv_one(self, interaction: discord.Interaction, button: discord.ui.Button, ctx: commands.Context):
        await interaction.response.send_message("Ton adversaire sera : 2")
        self.label = "adv['adv_name']"
        self.value = "adv['id']"
        await ctx.edit_message("adv['adv_name']")
        self.stop()
