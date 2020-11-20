import json
import urllib.request
# import logging
# from pathlib import Path
# from watchdog.observers import Observer
#
# from edlogwatcher import EDLogWatcher
# from edsession import (
#     classes,
# )
import requests


def load_config():
    with open('config.json') as fp:
        return json.load(fp)


def update_remote_data(src_dict: dict):
    src_dict['data'] = requests.get(src_dict['url']).json()


def lookup_module(module:str):
    module_lookup = {x.get('ed_symbol').lower(): x for x in config['eddb_data']['modules']['data']}
    return module_lookup[module]


config = load_config()
for entry in config['eddb_data'].values():
    update_remote_data(entry)

print(lookup_module('hpt_mrascanner_size0_class4'))

# logging.basicConfig(level=logging.INFO)
#
# log_dir = Path("~\\Saved Games\\Frontier Developments\\Elite Dangerous").expanduser()
# logging.info(f"Log Path: {log_dir}")
# # edlogwatcher = EDLogWatcher(log_dir=log_dir)
# session = classes.Overseer()
# logging.debug(f"Startup Overseer Object: {session.dict()}")
# # noinspection SpellCheckingInspection
# edlogwatcher = EDLogWatcher(session, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
# observer = Observer()
# observer.schedule(edlogwatcher, str(log_dir))
# logging.debug("Starting Observer...")
# observer.start()
# observer.join()
# logging.debug("Observer stopped")
