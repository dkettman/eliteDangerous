from loguru import logger

from watchdog.observers import Observer

import overseer

from edoverseer import classes

# logging.basicConfig(level=logging.DEBUG)

my_overseer = classes.Overseer()
# logging.debug(f"Startup Overseer Object: {session.dict()}")
# # noinspection SpellCheckingInspection
logwatcher = overseer.EDLogWatcher(my_overseer, ignore_regexes=[r".*cache", r".*~", r".*sw[px]"])
observer = Observer()
observer.schedule(logwatcher, str(classes.config['log_path']))
logger.debug("Starting Observer...")
observer.start()
observer.join()
logger.debug("Observer stopped")
