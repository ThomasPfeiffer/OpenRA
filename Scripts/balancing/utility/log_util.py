import logging


def get_logger(class_name):
    logger = logging.getLogger(class_name)
    ch = logging.StreamHandler()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(fmt='%(asctime)10s%(levelname)8s: %(message)s', datefmt='%I:%M:%S'))
    logger.addHandler(ch)
    return logger
