import logging


formatter = logging.Formatter(fmt='%(asctime)10s%(levelname)8s: %(message)s', datefmt='%I:%M:%S')
loggers = []


def add_handler(handler):
    handler.setFormatter(formatter)
    for logger in loggers:
        logger.addHandler(handler)


def get_logger(class_name):
    logger = logging.getLogger(class_name)
    ch = logging.StreamHandler()
    add_handler(ch)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    loggers.append(logger)
    return logger
