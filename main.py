import json
import logging
import os
import re
from pathlib import Path
from pprint import pprint

from watchdog.events import (
    FileModifiedEvent,
    RegexMatchingEventHandler,
)
from watchdog.observers import Observer

from edsession import (
    ed_enums,
    classes,
)

import PySimpleGUI as sg


class EDLogWatcher(RegexMatchingEventHandler):
    def __init__(self, edw: classes.Session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func_dict = {
            "EVENT_TYPE_CREATED": self.on_any_event,
            "EVENT_TYPE_MODIFIED": self.on_any_event,
            "Status": self.proc_status,
            "Cargo": self.proc_cargo,
            "Market": self.proc_market,
            # "EVENT_TYPE_DELETED": self.on_any_event,
            # "EVENT_TYPE_MOVED": self.on_any_event,
        }
        self._journal_func_dict = {
            "LoadGame": self.proc_journal_loadgame,
            "Loadout": self.proc_journal_loadout,
        }
        self.edw = edw
        self._journal_fp = ""
        self._loadout_entry = ""

    def proc_market(self, log_path: Path):
        pass

    def proc_cargo(self, log_path: Path):
        logging.debug(f"proc_cargo entered")
        with open(log_path, encoding="utf-8") as fp:
            lines = fp.read().replace("\n", "")
        data = json.loads(lines)
        logging.info(f"Cargo Data: {data}")
        self.edw.ship.inventory = []
        for i in data["Inventory"]:
            self.edw.ship.inventory.append(classes.Cargo.parse_obj(i))
        # for i in data["Inventory"]:
        #     self.edw.update_cargo(i)
        logging.info(f"Ship Cargo: {self.edw.ship.inventory}")

    def proc_status(self, log_path: Path):
        sf = ed_enums.StatusFlag
        with open(log_path, encoding="utf-8") as fp:
            lines = fp.readlines()
        # There should only ever be one line in this file, so this will grab that single line.
        data = json.loads(lines[0])
        # logging.debug(f"proc_status: {data}")
        flags = {}
        for flag in sf:
            is_set = bool(flag & data["Flags"])
            if is_set:
                flags[flag] = {is_set}
        self.edw.ship.status = flags
        pips = data.get("Pips", [0, 0, 0])
        self.edw.ship.pips = pips
        # self.edw.ship.fuel_level = data['Fuel']['FuelMain']

    def proc_journal(self, log_path: Path):
        # Initially, the file pointer for the Journal hasn't been
        # opened yet, so we need to open it and process it
        if self._journal_fp == "":
            self._journal_fp = open(log_path, "r", encoding="utf-8")

        # Now to process all of the lines in the log file
        buf = self._journal_fp.readlines()
        for line in buf:
            entry = json.loads(line)
            if entry["event"] in self._journal_func_dict.keys():
                self._journal_func_dict[entry["event"]](entry)

    def proc_journal_loadgame(self, entry):
        logging.debug(f"Loadgame Entry: {entry}")
        logging.debug(f"Ship_Localised: {entry['Ship_Localised']}")
        self.edw.commander = entry["Commander"]
        self.edw.credits = entry["Credits"]
        self.edw.ship.ship = entry["Ship"]
        self.edw.ship.ship_localised = entry["Ship_Localised"]
        self.edw.ship.ship_name = entry["ShipName"]
        self.edw.ship.ship_ident = entry["ShipIdent"]
        logging.debug(f"derp: {self.edw.ship.ship_localised}")

    def proc_journal_loadout(self, entry):
        logging.debug(f"Loadout Entry: {entry}")
        self.edw.ship = self.edw.ship.parse_obj(entry)
        self._loadout_entry = entry

    def on_any_event(self, event: FileModifiedEvent):
        evt_file_name = Path(event.src_path).name
        evt_file_stem = Path(event.src_path).stem
        evt_file_size = os.path.getsize(event.src_path)
        if evt_file_size == 0:
            logging.info(f"{evt_file_stem} - Truncated!")
            # pass
        else:
            logging.info(
                f"{evt_file_stem} is now {evt_file_size} bytes. -- {evt_file_stem}"
            )
            if evt_file_stem in self._func_dict:
                # noinspection PyArgumentList
                self._func_dict[evt_file_stem](event.src_path)
            elif re.match(r"Journal", str(evt_file_stem)):
                logging.info(f"Found a journal file: {evt_file_name}")
                self.proc_journal(event.src_path)
            else:
                logging.warning(f"No function for {evt_file_stem} yet")
        pprint(self.edw.dict(), indent=4)
        self.update_gui()

    def update_gui(self):
        window["commander"].update(f"{self.edw.commander}")
        window["credits"].update(f"{self.edw.credits}")
        window["ship_name"].update(
            f"{self.edw.ship.ship_name} - {self.edw.ship.ship_ident}"
        )
        window["ship_type"].update(f"{self.edw.ship.ship_localised}")


logging.basicConfig(level=logging.DEBUG)

# Setting up window
# sg.theme('DarkAmber')

layout = [
    [
        sg.Text("Commander Name:"),
        sg.Text("Waiting for data...", key="commander", size=(20, 1)),
        sg.Text("Credits:"),
        sg.Text(key="credits", size=(20, 1)),
    ],
    [
        sg.Text("Ship Name:"),
        sg.Text(key="ship_name", size=(40, 1)),
        sg.Text("Ship Type:"),
        sg.Text(key="ship_type", size=(40, 1)),
    ],
    [sg.OK()],
]

log_dir = Path("~\\Saved Games\\Frontier Developments\\Elite Dangerous").expanduser()
logging.info(f"Log Path: {log_dir}")
# edlogwatcher = EDLogWatcher(log_dir=log_dir)
session = classes.Session()
logging.debug(f"Startup Session Object: {session.dict()}")
# noinspection SpellCheckingInspection
edlogwatcher = EDLogWatcher(session, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
observer = Observer()
observer.schedule(edlogwatcher, str(log_dir))
logging.debug("Starting Observer...")
observer.start()

window = sg.Window("Elite: Dangerous Log Watcher", layout)
evt, val = window.read()

# observer.join()
logging.debug("Observer stopped")

window.close()
