import os
import discord
from discord.ui import View, Button
from discord.ext import commands
from db import *  # sqlite execute fonction =)


# Define a simple View that gives us a confirmation menu
class FightMenu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label='Battle', style=discord.ButtonStyle.green, emoji="⚔")
    async def battle(self, interaction, button):
        await interaction.response.edit_message(content='☣ Super !')
        self.value = 'battle'

    @discord.ui.button(label='Tes Stats', style=discord.ButtonStyle.green, emoji="💯")
    async def stats(self, interaction, button):
        await interaction.response.edit_message(content='☣ Voilà !')

    @discord.ui.button(label='Lvl_up', style=discord.ButtonStyle.green, emoji="🆙")
    async def lvlup(self, interaction, button):
        await interaction.response.edit_message(content='☣ Gere ton S.P.E.C.I.A.L !')

    @discord.ui.button(label='Adversaires', style=discord.ButtonStyle.blurple, emoji="👿")
    async def adv(self, interaction, button):
        await interaction.response.send_message(content='!adversaires')
        self.value = 'adversaires'

    @discord.ui.button(label='X', style=discord.ButtonStyle.red, emoji="<:incagay:710147834703511574>")
    async def quit(self, interaction, button):
        await interaction.response.edit_message(content='Bye bye', view=None)
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey ce menu n'est pas pour "
                                                    "toi, tape !menu si tu veux jouer "
                                                    "avec !", ephemeral=True)
            return False
        else:
            return True


class FightStart(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label='Oui', style=discord.ButtonStyle.green, emoji="<:incagay:710147834703511574>")
    async def confirm(self, interaction, button):
        # await interaction.response.send_message("C'est partie !")
        button.disabled = True
        await interaction.response.edit_message(content='☣ Super ! Tes adversaires  : ', view=None)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Non', style=discord.ButtonStyle.red, emoji='🙅')
    async def cancel(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(content='La prochaine fois 😉', view=None)
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey ce n'est pas ta partie", ephemeral=True)
            return False
        else:
            return True


class FightAdversary(View):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.adv_list = db_fight_get_adversary()
        for adv in self.adv_list:
            self.add_item(Button(label=f"{adv['adv_name']}", custom_id=f"{adv['id']}"))

    async def callback(self, interaction):
        await interaction.response.edit_message(content=f"tu as choisi", view=None)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Hey ce n'est pas ta partie", ephemeral=True)
            return False
        else:
            return True


class FightChoices(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(label='Attaquer', style=discord.ButtonStyle.green, emoji="⚔", custom_id='1')
    async def atk(self, interaction: discord.Interaction, button: discord.ui.Button):
        # await interaction.response.send_message('Too bad', ephemeral=True)
        await interaction.response.edit_message(content='Attaquer !!')
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

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Non non non!", ephemeral=True)
            return False
        else:
            return True
