# shepard_discord_bot

SuperBot est un bot Discord codé en Python utilisant la bibliothèque discord.py. Ce bot propose plusieurs fonctionnalités telles que la gestion de citations, des jeux et un mini-jeu de combat.


## Fonctionnalités
### Citation

    !qhelp: Affiche l'aide pour créer une citation.
    !qadd "citation" "nom de la personne": Ajoute une citation à la base de données.
    !qall: Affiche toutes les citations.
    !qr: Affiche une citation aléatoire.

### ### Combat

    !podium: Affiche le podium des joueurs de combat.
    !player_stat [membre]: Affiche les statistiques du joueur spécifié ou de l'auteur de la commande.
    !stats: Affiche les statistiques du joueur dans le Fight Club.
    !battle: Lance un mini-jeu de combat.

### Jeux

    !nb_magic: Un jeu où le joueur doit deviner un nombre secret.

## Prérequis

    Python 3.x
    Discord.py
    dotenv

### Installation


Installez les dépendances :

```
    pip install -r requirements.txt
```
Créez un fichier .env à la racine du projet et ajoutez les clés suivantes :

```
    PREFIX=!
    TOKEN=YOUR_DISCORD_BOT_TOKEN
```
### Utilisation

Exécutez le fichier main.py pour démarrer le bot :

```
    python main.py
```

## Structure du projet

    main.py: Fichier principal du bot Discord.
    bot_command.py: Gestion des commandes de citation.
    bot_battle.py: Gestion des commandes de combat.
    bot_games.py: Gestion des jeux.
    Buttons.py: Définition des boutons d'interaction pour le bot.
    db.py: Gestion de la base de donnée.

### Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.


## Auteur

Emmanuelle G. aka Ookamy