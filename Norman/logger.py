import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.handler = logging.FileHandler('log.log')
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger.addHandler(self.formatter)
        self.logger.addHandler(self.handler)

    def log_error(self, message):
        self.logger.error(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_debug(self, message):
        self.logger.debug(message)