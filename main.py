from source.src_01_SplashAppStarter import SplashAppStarter
from source.utils.LogManager import LogManager
import traceback
import sys


if __name__ == '__main__':
    logger = LogManager.get_logger()
    try:
        SplashAppStarter().start()

    except Exception as e:
        logger.critical(f"Unhandled exception in main: {e}", exc_info=True)
        traceback.print_exc()
        sys.exit(1)
