import logging
from yahtzee.events.event_broker import EventBroker


def logger_setup():
    """
    This class sets the formatting and the logging level of the logger for any file in the application
    To use the logger in any file, import logging and then instantiate the logger like so:
        log = logging.getLogger(__name__)

    Then to write a log to the stdout, use the logger like so:
        log.info("My log message")
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    logger_setup()
    broker = EventBroker()
    broker.start_server()
