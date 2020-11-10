import json
from pathlib import Path
from threading import Event, Thread

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class LogEvent(FileSystemEventHandler):
    def __init__(self, t_event: Event):
        self._t_event = t_event
        super().__init__()

    def on_modified(self, event):
        print("Caught modified event! {}".format(event))
        self._t_event.set()


class EDLogWatcher:
    def __init__(self, log_file: Path):
        print("Starting watcher for: {}".format(log_file))
        self._file_modified_event = Event()
        self._log_handle = log_file.open()
        # Creating the read lines handler
        self._read_file_thread = Thread(target=self.read_lines)
        # Way to get the thread to exit, will still need to set the event also so that
        # it loops one more time
        self._run = True
        self._read_file_thread.start()
        self._event_handler = LogEvent(self._file_modified_event)
        self._observer = Observer()
        # noinspection PyTypeChecker
        self._observer.schedule(self._event_handler, log_file)

    def handle_line(self, line: str):
        parsed = json.loads(line)
        print("Timestamp: {} -- Event: {}".format(parsed['timestamp'], parsed['event']))

    def read_lines(self):
        while self._run:
            # Wait for the event.set from LogEvent
            self._file_modified_event.wait()
            # Clear it immediately
            self._file_modified_event.clear()
            # If there aren't any new lines to read we get an empty array and nothing
            # is run
            for line in self._log_handle.readlines():
                self.handle_line(line)

    def _kill_line_reader(self):
        self._run = False
        self._file_modified_event.set()

log_dir = Path('c:\\Users\\chili\\Saved Games\\Frontier Developments\\Elite Dangerous')
watchme = EDLogWatcher(log_file=log_dir / 'Journal.201109145516.01.log')

# watchmen = {
#     'Cargo': EDLogWatcher(log_file=log_dir / 'Cargo.json'),
#     'Market': EDLogWatcher(log_file=log_dir / 'Market.json'),
#     'Modules': EDLogWatcher(log_file=log_dir / 'ModulesInfo.json'),
#     'NavRoute': EDLogWatcher(log_file=log_dir / 'NavRoute.json'),
#     'Outfitting': EDLogWatcher(log_file=log_dir / 'Outfitting.json'),
#     'Shipyard': EDLogWatcher(log_file=log_dir / 'Shipyard.json'),
#     'Status': EDLogWatcher(log_file=log_dir / 'Status.json')
# }


