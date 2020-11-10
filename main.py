import json
import time
from pathlib import Path
# from threading import Event, Thread

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

log_dir = Path('c:\\Users\\chili\\Saved Games\\Frontier Developments\\Elite Dangerous')

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(" - {}".format(event))

if __name__ == "__main__":
    log_dir = Path('c:\\Users\\chili\\Saved Games\\Frontier Developments\\Elite Dangerous')
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, log_dir.absolute(), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

#watchme = EDLogWatcher(log_file=log_dir / 'Journal.201109145516.01.log')

# watchmen = {
#     'Cargo': EDLogWatcher(log_file=log_dir / 'Cargo.json'),
#     'Market': EDLogWatcher(log_file=log_dir / 'Market.json'),
#     'Modules': EDLogWatcher(log_file=log_dir / 'ModulesInfo.json'),
#     'NavRoute': EDLogWatcher(log_file=log_dir / 'NavRoute.json'),
#     'Outfitting': EDLogWatcher(log_file=log_dir / 'Outfitting.json'),
#     'Shipyard': EDLogWatcher(log_file=log_dir / 'Shipyard.json'),
#     'Status': EDLogWatcher(log_file=log_dir / 'Status.json')
# }


