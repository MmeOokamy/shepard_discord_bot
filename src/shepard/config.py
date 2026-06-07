# coding: utf-8
"""Configuration centrale : chemins absolus, variables d'environnement et IDs Discord."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Racine du projet : src/shepard/config.py -> remonte de 3 niveaux
BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

# ----- Chemins -----
DB_PATH = str(BASE_DIR / "shepard.db")
SQL_DIR = BASE_DIR / "sql"
INIT_SQL_PATH = str(SQL_DIR / "init.sql")
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
LOG_DIR = BASE_DIR / "logs"

# ----- Environnement -----
PREFIX = os.getenv("PREFIX")
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else None

# ----- Salons Discord -----
TEST_CHANNEL_ID = 1031895034439675986
PROD_CHANNEL_ID = 861613275414528030


def img_path(filename):
    """Chemin absolu d'une image de assets/img."""
    return str(IMG_DIR / filename)
