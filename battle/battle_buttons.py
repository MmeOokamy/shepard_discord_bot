import os
import discord
from discord.ext import commands


# Define a simple View that gives us a confirmation menu
class FightMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Battle', style=discord.ButtonStyle.green, emoji="⚔")
    async def battle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content='☣ Super !')
        self.value = 'battle'
        self.stop()

    @discord.ui.button(label='Tes Stats', style=discord.ButtonStyle.primary, emoji="💯")
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content='☣ Super !')
        self.value = 'stats'
        self.stop()

    @discord.ui.button(label='LVL UP', style=discord.ButtonStyle.primary, emoji="🆙", disabled=True)
    async def lvl_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content='☣ Super !')
        self.value = 'lvlup'
        button.disabled = True
        self.stop()

    @discord.ui.button(label='Adversaires', style=discord.ButtonStyle.blurple, emoji="👿")
    async def adv(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content='☣ La liste : ')
        self.value = 'adversaires'
        self.stop()


class FightStart(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Oui', style=discord.ButtonStyle.green, emoji="<:incagay:710147834703511574>")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message("C'est partie !")
        button.disabled = True
        await interaction.response.edit_message(content='☣ Super ! Tu peux choisir ton adversaire  : ', view=None)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Non', style=discord.ButtonStyle.red, emoji='🙅')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(content='La prochaine fois 😉', view=None)
        self.value = False
        self.stop()


class FightChoices(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Attaquer', style=discord.ButtonStyle.green, emoji="⚔", custom_id='1')
    async def atk(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message('Too bad', ephemeral=True)
        await interaction.response.edit_message('Attaquer !!')
        self.value = 1
        self.stop()

    @discord.ui.button(label='Heal', style=discord.ButtonStyle.green, emoji="🧪", custom_id='2')
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message('Too bad', ephemeral=True)
        self.value = 2
        self.stop()

    @discord.ui.button(label='Etats', style=discord.ButtonStyle.green, emoji="🧬", custom_id='3')
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message('Too bad', ephemeral=True)
        self.value = 3
        self.stop()
