import logging


formatter = logging.Formatter(fmt='%(asctime)10s%(levelname)8s: %(message)s', datefmt='%I:%M:%S')
loggers = []


def get_logger(class_name):
    logger = logging.getLogger(class_name)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    loggers.append(logger)
    return logger
