import json
import logging
import os
import re
from pathlib import Path

from watchdog.events import RegexMatchingEventHandler, FileModifiedEvent

from edoverseer import classes, ed_enums


class EDLogWatcher(RegexMatchingEventHandler):
    def __init__(self, overseer: classes.Overseer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func_dict = {
            "EVENT_TYPE_CREATED": self.on_any_event,
            "EVENT_TYPE_MODIFIED": self.on_any_event,
            # "Status": self.proc_status,
            # "Cargo": self.proc_cargo,
            # "Market": self.proc_market,
            # "EVENT_TYPE_DELETED": self.on_any_event,
            # "EVENT_TYPE_MOVED": self.on_any_event,
        }
        self._journal_func_dict = {
            "LoadGame": self.proc_journal_loadgame,
            "Loadout": self.proc_journal_loadout,
            "Materials": self.proc_journal_materials,
        }
        self.overseer = overseer
        self._journal_fp = ""

    def proc_market(self, log_path: Path):
        pass

    def proc_cargo(self, log_path: Path):
        with open(log_path, encoding="utf-8") as fp:
            lines = fp.read().replace("\n", "")
        data = json.loads(lines)
        self.overseer.ship.inventory = []
        for i in data["Inventory"]:
            self.overseer.ship.inventory.append(classes.Cargo.parse_obj(i))

    def proc_status(self, log_path: Path):
        sf = ed_enums.StatusFlag
        with open(log_path, encoding="utf-8") as fp:
            lines = fp.readlines()
        # There should only ever be one line in this file, so this will grab that single line.
        data = json.loads(lines[0])
        flags = {}
        for flag in sf:
            is_set = bool(flag & data["Flags"])
            if is_set:
                flags[flag] = {is_set}
        self.overseer.ship.status = flags
        pips = data.get("Pips", [0, 0, 0])
        self.overseer.ship.pips = pips

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
        self.overseer.commander = entry["Commander"]
        self.overseer.credits = entry["Credits"]
        self.overseer.ship.ship = entry["Ship"]
        self.overseer.ship.ship_localised = entry["Ship_Localised"]
        self.overseer.ship.ship_name = entry["ShipName"]
        self.overseer.ship.ship_ident = entry["ShipIdent"]

    def proc_journal_loadout(self, entry):
        self.overseer.ship = self.overseer.ship.copy(update=entry)
        self.overseer.ship.update_modules(entry["Modules"])
        # pprint.pprint(self.overseer.dict())

    def proc_journal_materials(self, entry):
        self.overseer.ship.update_materials(entry)

    def on_any_event(self, event: FileModifiedEvent):
        # evt_file_name = Path(event.src_path).name
        evt_file_stem = Path(event.src_path).stem
        evt_file_size = os.path.getsize(event.src_path)
        if evt_file_size == 0:
            logging.debug(f"{evt_file_stem} - Truncated!")
            # pass
        else:
            logging.debug(
                f"{evt_file_stem} is now {evt_file_size} bytes. -- {evt_file_stem}"
            )
            if evt_file_stem in self._func_dict:
                self._func_dict[evt_file_stem](event.src_path)
            elif re.match(r'Journal.', str(evt_file_stem)):
                self.proc_journal(event.src_path)
            else:
                logging.warning(f"No function for {evt_file_stem} yet")
