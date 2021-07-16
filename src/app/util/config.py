import logging
import yaml


class Config:
    def __init__(self, path="config.yaml"):
        self.log = logging.getLogger(__name__)
        self.__config = yaml.load(open(path), Loader=yaml.Loader)
        self.HOST = self.__config["host"]
        self.PORT = self.__config["port"]
        self.LOG_LEVEL = self.set_log_level()

    def set_log_level(self):
        log_level_map = {
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG
        }
        return log_level_map[self.__config["log_level"]]

    def log_config_settings(self):
        self.log.info(f"HOST: {self.HOST}")
        self.log.info(f"PORT: {self.PORT}")
