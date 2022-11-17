import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": "app.log",
            "encoding" : "UTF-8"
        }
    },
    "loggers": {
        "importApp": {
            "handlers": ["fileHandler"],
            #"level": "DEBUG",
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('importApp')
logger.debug('debug log')