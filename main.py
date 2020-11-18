import json
import logging
import os
import re
import sys
from pathlib import Path
from pprint import pprint

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QMainWindow, QApplication, QAction, QLabel, QTreeWidgetItem, QAbstractItemView
from watchdog.events import (
    FileModifiedEvent,
    RegexMatchingEventHandler,
)
from watchdog.observers import Observer

from edsession import (
    ed_enums,
    classes,
)
from mainUI import Ui_MainWindow


class EDLogWatcher(RegexMatchingEventHandler):
    def __init__(self, edw: classes.Session, ui: QMainWindow, *args, **kwargs):
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
        self.ui = ui
        self._journal_fp = ""
        # self._loadout_entry = ""

    def proc_market(self, log_path: Path):
        pass

    def proc_cargo(self, log_path: Path):
        logging.debug(f"proc_cargo entered")
        with open(log_path, encoding='utf-8') as fp:
            lines = fp.read().replace("\n", "")
        data = json.loads(lines)
        logging.info(f"Cargo Data: {data}")
        self.edw.ship.inventory = []
        for i in data['Inventory']:
            self.edw.ship.inventory.append(classes.Cargo.parse_obj(i))
        # for i in data["Inventory"]:
        #     self.edw.update_cargo(i)
        #logging.info(f"Ship Cargo: {self.edw.ship.inventory}")


    def proc_status(self, log_path: Path):
        sf = ed_enums.StatusFlag
        with open(log_path, encoding='utf-8') as fp:
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
            self._journal_fp = open(log_path, "r", encoding='utf-8')

        # Now to process all of the lines in the log file
        buf = self._journal_fp.readlines()
        for line in buf:
            entry = json.loads(line)
            if entry["event"] in self._journal_func_dict.keys():
                self._journal_func_dict[entry["event"]](entry)

    def proc_journal_loadgame(self, entry):
        logging.debug(f"Loadgame Entry: {entry}")
        self.edw.commander = entry['Commander']
        self.edw.credits = entry['Credits']
        self.edw.ship.ship = entry['Ship']
        self.edw.ship.ship_localised = entry['Ship_Localised']
        self.edw.ship.ship_name = entry['ShipName']
        self.edw.ship.ship_ident = entry['ShipIdent']
        self.ui.ui.lbl_commander.setText(self.edw.commander)
        self.ui.ui.lbl_credits.setText(f"{self.edw.credits:,}")
        self.ui.ui.lbl_ship_name.setText(f"{self.edw.ship.ship_name} [{self.edw.ship.ship_ident}]")
        self.ui.ui.lbl_ship_type.setText(self.edw.ship.ship_localised)

    def proc_journal_loadout(self, entry):
        logging.debug(f"Loadout Entry: {entry}")
        self.edw.ship = self.edw.ship.copy(update=entry)
        pprint(entry)
        # self._loadout_entry = entry

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
        # pprint(self.edw.ship.dict(), indent=4)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tree_loadout.setSelectionBehavior(QAbstractItemView.SelectRows)

        model_tree_loadout = QStandardItemModel()
        model_tree_loadout.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
        self.ui.tree_loadout.setModel(model_tree_loadout)
        self.ui.tree_loadout.setUniformRowHeights(True)

        for i in range(3):
            parent1 = QStandardItem('Family {}. Some long status text for sp'.format(i))
            for j in range(3):
                child1 = QStandardItem('Child {}'.format(i*3+j))
                child2 = QStandardItem('row: {}, col: {}'.format(i, j+1))
                child3 = QStandardItem('row: {}, col: {}'.format(i, j+2))
                parent1.appendRow([child1, child2, child3])
            model_tree_loadout.appendRow(parent1)
            self.ui.tree_loadout.setFirstColumnSpanned(i, self.ui.tree_loadout.rootIndex(), True)
        index = model_tree_loadout.indexFromItem(parent1)
        self.ui.tree_loadout.expand(index)
        self.ui.tree_loadout.show()

    def update_commander(self, name=None):
        self.ui.lbl_commander.setText(name)



logging.basicConfig(level=logging.INFO)

log_dir = Path("~\\Saved Games\\Frontier Developments\\Elite Dangerous").expanduser()
logging.info(f"Log Path: {log_dir}")
# edlogwatcher = EDLogWatcher(log_dir=log_dir)
session = classes.Session()
logging.debug(f"Startup Session Object: {session.dict()}")
# noinspection SpellCheckingInspection

app = QApplication(sys.argv)
window = MainWindow()
window.show()

edlogwatcher = EDLogWatcher(session, ui=window, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
observer = Observer()
observer.schedule(edlogwatcher, str(log_dir))
logging.debug("Starting Observer...")
observer.start()
# observer.join()


logging.debug("Observer stopped")
sys.exit(app.exec_())

