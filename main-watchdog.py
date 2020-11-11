import json
import os
import status_enums

from pathlib import Path
from watchdog.events import (
    FileModifiedEvent,
    RegexMatchingEventHandler,
)
from watchdog.observers import Observer


class EDWatcher:
    def __init__(self, *args, **kwargs):
        self._pips = {"sys": "", "eng": "", "wep": ""}
        self._status_flags = {}
        self._legal_state = ""
        self._cargo_cur = 0
        self._cargo_max = 0
        self._fuel_cur = 0
        self._fuel_max = 0
        self._cargo_hold = {}

    def set_status_flags(self, flags: dict):
        # print(f"set_status_flags - Received: {flags}")
        self._status_flags = flags

    def set_pip(self, sys: str, pips: int):
        # print(f"set_pip - Received: {sys}, {pips}")
        self._pips[sys] = pips

    def get_pip(self, sys: str):
        return status_enums.SystemPips.power_pips[self._pips[sys]]

    def set_cargo_max(self,max: int):
        self._cargo_max = max

    def get_cargo_max(self):
        return self._cargo_max

    def set_cargo_cur(self,cur: int):
        self._cargo_cur = cur

    def get_cargo_cur(self):
        return self._cargo_cur

    def reset_cargo(self):
        self._cargo_hold = {}

    def update_cargo(self, cargo: dict):
        self._cargo_hold[cargo['Name']] = cargo['Count']

    def get_cargo(self):
        return self._cargo_hold


class EDLogWatcher(RegexMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._func_dict = {
            "EVENT_TYPE_CREATED": self.on_any_event,
            "EVENT_TYPE_DELETED": self.on_any_event,
            "EVENT_TYPE_MODIFIED": self.on_any_event,
            "EVENT_TYPE_MOVED": self.on_any_event,
            "Status": self.proc_status,
            "Cargo": self.proc_cargo,
            # "Market": self.proc_market,
        }
        self.edw = EDWatcher()

    def proc_market(self, log_path: Path):
        print(f"Market Schtuff goes here")

    def proc_cargo(self, log_path: Path):
        # Update Cargo
        self.edw.reset_cargo()
        used_cargo = 0
        with open(log_path) as fp:
            lines = fp.read().replace('\n', '')
        data = json.loads(lines)
        for i in data['Inventory']:
            used_cargo += i['Count']
            self.edw.update_cargo(i)
        self.edw.set_cargo_cur(used_cargo)

        # Update contents of Cargo Hold


    def proc_status(self, log_path: Path):
        sf = status_enums.StatusFlag
        with open(log_path) as fp:
            lines = fp.readlines()
        # There should only ever be one line in this file, so this will grab that single line.
        data = json.loads(lines[0])
        flags = {}
        for flag in sf:
            is_set = bool(flag & data["Flags"])
            if is_set:
                flags[flag] = {is_set}
        self.edw.set_status_flags(flags)
        self.edw.set_pip("sys", data["Pips"][0])
        self.edw.set_pip("eng", data["Pips"][1])
        self.edw.set_pip("wep", data["Pips"][2])

    def on_any_event(self, event: FileModifiedEvent):
        evt_file_name = Path(event.src_path).name
        evt_file_stem = Path(event.src_path).stem
        evt_file_size = os.path.getsize(event.src_path)
        if evt_file_size == 0:
            # print(f"{evt_file_stem} - Truncated!")
            pass
        else:
            # print(f"{evt_file_stem} is now {evt_file_size} bytes. -- {evt_file_stem}")
            if evt_file_stem in self._func_dict:
                self._func_dict[evt_file_stem](event.src_path)
            else:
                print(f"No function for {evt_file_stem} yet")


log_dir = Path("c:\\Users\\chili\\Saved Games\\Frontier Developments\\Elite Dangerous")
# edlogwatcher = EDLogWatcher(log_dir=log_dir)
edlogwatcher = EDLogWatcher()
observer = Observer()
observer.schedule(edlogwatcher, str(log_dir))
observer.start()
