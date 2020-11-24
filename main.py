import logging

from watchdog.observers import Observer

import logwatcher
#
# from edlogwatcher import EDLogWatcher
# from edoverseer import (
#     classes,
# )
from edoverseer import classes

logging.basicConfig(level=logging.DEBUG)

overseer = classes.Overseer()
# logging.debug(f"Startup Overseer Object: {session.dict()}")
# # noinspection SpellCheckingInspection
logwatcher = logwatcher.EDLogWatcher(overseer, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
observer = Observer()
observer.schedule(logwatcher, str(classes.config['log_path']))
logging.debug("Starting Observer...")
observer.start()
observer.join()
logging.debug("Observer stopped")
