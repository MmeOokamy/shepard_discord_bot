# coding: utf-8
"""Utilitaires système (état des services systemd)."""
import subprocess


def check_service_status(service_name):
    """Vérifie l'état d'un service systemd. Retourne True si actif."""
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout.strip() == "active"
    except Exception:
        return False
