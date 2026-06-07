import discord

from shepard.db.fight import db_fight_get_adversary


# Define a simple View that gives us a confirmation menu
class FightMenu(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Battle", style=discord.ButtonStyle.green, emoji="⚔")
    async def battle(self, interaction, button):
        await interaction.response.edit_message(content="☣ Super !")
        self.value = "battle"

    @discord.ui.button(label="Tes Stats", style=discord.ButtonStyle.green, emoji="💯")
    async def stats(self, interaction, button):
        await interaction.response.edit_message(content="☣ Voilà !")

    @discord.ui.button(label="Lvl_up", style=discord.ButtonStyle.green, emoji="🆙")
    async def lvlup(self, interaction, button):
        await interaction.response.edit_message(content="☣ Gere ton S.P.E.C.I.A.L !")

    @discord.ui.button(
        label="Adversaires", style=discord.ButtonStyle.blurple, emoji="👿"
    )
    async def adv(self, interaction, button):
        await interaction.response.send_message(content="!adversaires")
        self.value = "adversaires"

    @discord.ui.button(
        label="X", style=discord.ButtonStyle.red, emoji="<:incagay:710147834703511574>"
    )
    async def quit(self, interaction, button):
        await interaction.response.edit_message(content="Bye bye", view=None)
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "Hey ce menu n'est pas pour "
                "toi, tape !menu si tu veux jouer "
                "avec !",
                ephemeral=True,
            )
            return False
        else:
            return True


class FightStart(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(
        label="Oui",
        style=discord.ButtonStyle.green,
        emoji="<:incagay:710147834703511574>",
    )
    async def confirm(self, interaction, button):
        # await interaction.response.send_message("C'est partie !")
        button.disabled = True
        await interaction.response.edit_message(
            content="☣ Super ! Tes adversaires  : ", view=None
        )
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label="Non", style=discord.ButtonStyle.red, emoji="🙅")
    async def cancel(self, interaction, button):
        button.disabled = True
        await interaction.response.edit_message(
            content="La prochaine fois 😉", view=None
        )
        self.value = False
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "Hey ce n'est pas ta partie", ephemeral=True
            )
            return False
        else:
            return True


class FightAdversary(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    emoji = ("❓", "🧸", "👿", "⚔", "☣")
    advs = db_fight_get_adversary()

    @discord.ui.button(
        label=f"Aléatoire", style=discord.ButtonStyle.blurple, emoji=emoji[0]
    )
    async def adv_random(self, interaction, button):
        await interaction.response.edit_message(
            content=f"Merci d'accueillir :  {self.emoji[0]}", view=None
        )
        self.value = 0
        self.stop()

    @discord.ui.button(
        label=f"{advs[0]['name']}", style=discord.ButtonStyle.blurple, emoji=emoji[1]
    )
    async def adv_one(self, interaction, button):
        await interaction.response.edit_message(
            content=f"Merci d'accueillir :  {self.emoji[1]}", view=None
        )
        self.value = 1
        self.stop()

    @discord.ui.button(
        label=f"{advs[1]['name']}", style=discord.ButtonStyle.gray, emoji=emoji[2]
    )
    async def adv_two(self, interaction, button):
        await interaction.response.edit_message(
            content=f"Merci d'accueillir :  {self.emoji[2]}", view=None
        )
        self.value = 2
        self.stop()

    @discord.ui.button(
        label=f"{advs[2]['name']}", style=discord.ButtonStyle.green, emoji=emoji[3]
    )
    async def adv_tree(self, interaction, button):
        await interaction.response.edit_message(
            content=f"Merci d'accueillir :  {self.emoji[3]}", view=None
        )
        self.value = 3
        self.stop()

    @discord.ui.button(
        label=f"{advs[3]['name']}", style=discord.ButtonStyle.red, emoji=emoji[4]
    )
    async def adv_four(self, interaction, button):
        await interaction.response.edit_message(
            content=f"Merci d'accueillir :  {self.emoji[4]}", view=None
        )
        self.value = 4
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(
                "Hey ce n'est pas ta partie", ephemeral=True
            )
            return False
        else:
            return True


class FightChoices(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.value = None
        self.ctx = ctx

    @discord.ui.button(
        label="Attaquer", style=discord.ButtonStyle.green, emoji="⚔", custom_id="1"
    )
    async def atk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Attaquer !!", view=None)
        self.value = 1
        self.stop()

    @discord.ui.button(
        label="Heal", style=discord.ButtonStyle.green, emoji="🧪", custom_id="2"
    )
    async def heal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="Une petite boisson fraîche?!!", view=None
        )
        self.value = 2
        self.stop()

    @discord.ui.button(
        label="Stats", style=discord.ButtonStyle.green, emoji="🧬", custom_id="3"
    )
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="🧮", view=None)
        self.value = 3
        self.stop()

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("Non non non!", ephemeral=True)
            return False
        else:
            return True
