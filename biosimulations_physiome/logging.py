import logging 
def setup_logging(log_level=logging.DEBUG, log_file="log.txt", log_file_level=logging.WARN):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_file_level)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


