import logging


def get_logger(logLevel=logging.DEBUG):
    log_format = "[%(levelname)7s][%(asctime)s][%(filename)20s:%(lineno)4s:%(funcName)20s()] -  %(message)s"
    logging.basicConfig(level=logLevel, format=log_format)
    return logging
