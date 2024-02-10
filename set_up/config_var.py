import os
import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)

PATH = __file__.replace("/config_var.py", "").replace("/set_up", "").replace("\\", "/")
REPOPATH = "Andrecuogh/Progetto-Schedina"

VERSION = 0.4

TOKEN = "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"


def write_config(foldpath, lat_day):
    from set_up.league_data import postponed_days, postponed_matches

    config_dict = {
        "VERSION": VERSION,
        "MATCHDAY": lat_day,
        "POSTPONED DAYS": postponed_days,
        "POSTPONED MATCHES": postponed_matches,
    }
    with open(f"{foldpath}/set_up/config_app.txt", "w") as file:
        for key, value in config_dict.items():
            file.write(f"{key} = {value}\n")
