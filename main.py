import logging

from watchdog.observers import Observer

import edlogwatcher
#
# from edlogwatcher import EDLogWatcher
# from edsession import (
#     classes,
# )
from edsession import classes

logging.basicConfig(level=logging.DEBUG)

overseer = classes.Overseer()
# logging.debug(f"Startup Overseer Object: {session.dict()}")
# # noinspection SpellCheckingInspection
logwatcher = edlogwatcher.EDLogWatcher(overseer, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
observer = Observer()
observer.schedule(logwatcher, str(classes.config['log_path']))
logging.debug("Starting Observer...")
observer.start()
observer.join()
logging.debug("Observer stopped")
