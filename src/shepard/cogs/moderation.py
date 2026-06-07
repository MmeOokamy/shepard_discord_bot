# coding: utf-8
"""Commandes de ménage des salons (réservées à l'owner via @is_me)."""
import logging

import discord
from discord import app_commands
from discord.ext import commands

from shepard.core.checks import is_me

logger = logging.getLogger("discord_bot.moderation")

# Profondeur de recherche max pour clear_user (nb de messages parcourus)
SEARCH_DEPTH = 1000


class ConfirmView(discord.ui.View):
    """Petit menu de confirmation Confirmer / Annuler."""

    def __init__(self, author, timeout=20):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.edit_message(content="Suppression en cours...", view=None)
        self.stop()

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.edit_message(content="Annulé.", view=None)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message(
                "Cette confirmation n'est pas pour toi.", ephemeral=True
            )
            return False
        return True


class ClearAllView(discord.ui.View):
    """Choix de la méthode pour vider entièrement un salon."""

    def __init__(self, author, can_clone=True, can_purge=True, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None  # None=timeout, "cancel", "clone" ou "purge"
        for child in self.children:
            if child.label == "Clone + suppression" and not can_clone:
                child.disabled = True
            elif child.label == "Purge en boucle" and not can_purge:
                child.disabled = True

    @discord.ui.button(label="Clone + suppression", style=discord.ButtonStyle.danger, emoji="♻️")
    async def clone_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "clone"
        await interaction.response.edit_message(
            content="♻️ Clone + suppression en cours...", view=None
        )
        self.stop()

    @discord.ui.button(label="Purge en boucle", style=discord.ButtonStyle.primary, emoji="🧹")
    async def purge_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "purge"
        await interaction.response.edit_message(
            content="🧹 Purge en cours... ça peut prendre un moment.", view=None
        )
        self.stop()

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.secondary)
    async def cancel_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "cancel"
        await interaction.response.edit_message(content="Annulé.", view=None)
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message(
                "Cette action n'est pas pour toi.", ephemeral=True
            )
            return False
        return True


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} --- OK")

    @staticmethod
    def _bot_can_manage(channel):
        """Le bot a-t-il 'Gérer les messages' dans ce salon ?"""
        return channel.permissions_for(channel.guild.me).manage_messages

    # ------------------------------------------------------------------ #
    #  Messages                                                          #
    # ------------------------------------------------------------------ #
    @commands.hybrid_command(
        name="clear",
        description="Supprime les N derniers messages (salon courant ou ciblé).",
    )
    @app_commands.describe(
        amount="Nombre de messages à supprimer",
        channel="Salon ciblé (par défaut : le salon courant)",
    )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    @is_me()
    async def clear(self, ctx, amount: int, channel: discord.TextChannel = None):
        if amount < 1:
            await ctx.send("Indique un nombre de messages ≥ 1.", delete_after=5)
            return
        target = channel or ctx.channel
        if not self._bot_can_manage(target):
            await ctx.send(
                f"⛔ Il me manque 'Gérer les messages' dans {target.mention}.",
                delete_after=8,
            )
            return

        await ctx.defer()
        is_prefix = ctx.interaction is None
        # en prefix uniquement, on efface aussi le message de la commande s'il est dans la cible
        extra = 1 if (is_prefix and target == ctx.channel) else 0
        deleted = await target.purge(limit=amount + extra)
        count = max(0, len(deleted) - extra)
        if is_prefix and target != ctx.channel:
            await ctx.message.delete()

        await ctx.send(
            f"🧹 {count} message(s) supprimé(s) dans {target.mention}.", delete_after=5
        )
        logger.info(f"{ctx.author} a purgé {count} messages dans #{target}")

    @commands.hybrid_command(
        name="clear_user",
        description="Supprime jusqu'à N messages d'un membre.",
    )
    @app_commands.describe(
        member="Membre dont on supprime les messages",
        amount="Nombre maximum de messages à supprimer",
        channel="Salon ciblé (par défaut : le salon courant)",
    )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    @is_me()
    async def clear_user(
        self, ctx, member: discord.Member, amount: int = 50, channel: discord.TextChannel = None
    ):
        if amount < 1:
            await ctx.send("Indique un nombre de messages ≥ 1.", delete_after=5)
            return
        target = channel or ctx.channel
        if not self._bot_can_manage(target):
            await ctx.send(
                f"⛔ Il me manque 'Gérer les messages' dans {target.mention}.",
                delete_after=8,
            )
            return

        await ctx.defer()
        remaining = amount

        def check(message):
            nonlocal remaining
            if message.author == member and remaining > 0:
                remaining -= 1
                return True
            return False

        if ctx.interaction is None:
            await ctx.message.delete()
        deleted = await target.purge(limit=SEARCH_DEPTH, check=check)
        await ctx.send(
            f"🧹 {len(deleted)} message(s) de {member.display_name} supprimé(s) "
            f"dans {target.mention}.",
            delete_after=5,
        )
        logger.info(
            f"{ctx.author} a purgé {len(deleted)} messages de {member} dans #{target}"
        )

    @staticmethod
    async def _purge_all(channel):
        """Vide un salon par purges successives. Retourne le nombre supprimé."""
        total = 0
        while True:
            deleted = await channel.purge(limit=100)
            total += len(deleted)
            if len(deleted) < 100:
                break
        return total

    @staticmethod
    async def _clone_and_delete(ctx, channel):
        """Recrée le salon à l'identique puis supprime l'original. Retourne le clone."""
        position = channel.position
        clone = await channel.clone(reason=f"clearall par {ctx.author}")
        await channel.delete(reason=f"clearall par {ctx.author}")
        try:
            await clone.edit(position=position)
        except discord.HTTPException:
            pass
        return clone

    @commands.hybrid_command(
        name="clearall",
        description="Vide entièrement un salon (méthode au choix : clone ou purge).",
    )
    @app_commands.describe(channel="Salon à vider (par défaut : le salon courant)")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    @is_me()
    async def clearall(self, ctx, channel: discord.TextChannel = None):
        target = channel or ctx.channel
        me = target.guild.me
        can_purge = target.permissions_for(me).manage_messages
        can_clone = (
            me.guild_permissions.manage_channels
            and target.permissions_for(me).manage_channels
        )

        if not can_purge and not can_clone:
            await ctx.send(
                f"⛔ Il me manque les permissions pour vider {target.mention} "
                f"('Gérer les messages' ou 'Gérer les salons').",
                delete_after=8,
            )
            return

        view = ClearAllView(ctx.author, can_clone=can_clone, can_purge=can_purge)
        prompt = await ctx.send(
            f"⚠️ Vider **entièrement** {target.mention} ? Choisis la méthode :",
            view=view,
        )
        await view.wait()

        if view.value is None:
            await prompt.edit(content="⏳ Temps écoulé, action annulée.", view=None)
            return
        if view.value == "cancel":
            return

        deleting_current = target == ctx.channel

        if view.value == "clone":
            name = target.name
            clone = await self._clone_and_delete(ctx, target)
            logger.info(f"{ctx.author} a vidé #{name} (clone) -> nouveau salon {clone.id}")
            if deleting_current:
                await clone.send(
                    f"🧼 Salon vidé (recréé à l'identique) par {ctx.author.mention}."
                )
            else:
                await ctx.send(
                    f"🧼 {clone.mention} vidé (clone + suppression).", delete_after=8
                )
        else:  # purge
            total = await self._purge_all(target)
            logger.info(f"{ctx.author} a vidé #{target} (purge, {total} messages)")
            if deleting_current:
                await target.send(f"🧼 {total} message(s) supprimé(s).", delete_after=8)
            else:
                await ctx.send(
                    f"🧼 {target.mention} vidé ({total} message(s)).", delete_after=8
                )

    @commands.hybrid_command(
        name="delmsg",
        description="Supprime un message précis (par ID, ou en répondant au message en prefix).",
    )
    @app_commands.describe(message_id="ID du message à supprimer")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    @is_me()
    @commands.bot_has_permissions(manage_messages=True)
    async def delmsg(self, ctx, message_id: str = None):
        target = None
        # réponse à un message : disponible uniquement en mode prefix
        if ctx.interaction is None and ctx.message.reference is not None:
            ref = ctx.message.reference
            target = ref.resolved or await ctx.channel.fetch_message(ref.message_id)
        elif message_id is not None:
            target = await ctx.channel.fetch_message(int(message_id))

        if target is None:
            await ctx.send(
                "Donne l'ID du message, ou réponds au message à supprimer.",
                delete_after=8,
            )
            return

        await target.delete()
        if ctx.interaction is None:
            await ctx.message.delete()
        await ctx.send("🗑️ Message supprimé.", delete_after=5)
        logger.info(f"{ctx.author} a supprimé le message {target.id} dans #{ctx.channel}")

    # ------------------------------------------------------------------ #
    #  Salons                                                            #
    # ------------------------------------------------------------------ #
    @commands.hybrid_command(
        name="delchannel",
        description="Supprime un salon (le salon courant si non précisé). Confirmation requise.",
    )
    @app_commands.describe(channel="Salon à supprimer (par défaut : le salon courant)")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.guild_only()
    @is_me()
    @commands.bot_has_permissions(manage_channels=True)
    async def delchannel(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        deleting_current = channel == ctx.channel

        view = ConfirmView(ctx.author)
        prompt = await ctx.send(
            f"⚠️ Supprimer définitivement {channel.mention} ? "
            f"Cette action est **irréversible**.",
            view=view,
        )
        await view.wait()

        if view.value is None:
            await prompt.edit(content="⏳ Temps écoulé, suppression annulée.", view=None)
            return
        if view.value is False:
            return  # le bouton Annuler a déjà édité le message

        name = channel.name
        await channel.delete(reason=f"Demandé par {ctx.author}")
        logger.info(f"{ctx.author} a supprimé le salon #{name}")
        if not deleting_current:
            await ctx.send(f"🗑️ Salon #{name} supprimé.")

    # ------------------------------------------------------------------ #
    #  Gestion des erreurs                                               #
    # ------------------------------------------------------------------ #
    async def cog_command_error(self, ctx, error):
        # BotMissingPermissions est une sous-classe de CheckFailure -> à tester avant
        if isinstance(error, commands.BotMissingPermissions):
            perms = ", ".join(error.missing_permissions)
            await ctx.send(f"⛔ Il me manque la permission : {perms}.", delete_after=8)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("⛔ Commande réservée à l'owner.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❓ Argument manquant : `{error.param.name}`.", delete_after=8)
        elif isinstance(error, (commands.BadArgument, commands.MemberNotFound, commands.ChannelNotFound)):
            await ctx.send("❓ Argument invalide (membre, salon ou nombre).", delete_after=8)
        elif isinstance(error, discord.NotFound):
            await ctx.send("Introuvable (message ou salon déjà supprimé ?).", delete_after=8)
        elif isinstance(error, discord.Forbidden):
            await ctx.send("⛔ Discord refuse l'action (permissions/hiérarchie).", delete_after=8)
        else:
            logger.error(f"Erreur dans une commande de modération : {error}")
            raise error


async def setup(bot):
    try:
        await bot.add_cog(Moderation(bot))
        logger.info("Module Moderation ajouté avec succès")
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du module Moderation : {e}")
