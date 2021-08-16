import logging


def init_logger(name, loglevel=logging.INFO, filepath=None):
    _logger = logging.getLogger(name)
    logging.basicConfig(
        format='%(asctime)s %(module)s:%(lineno)s %(levelname)s %',
        level=loglevel
    )
    return _logger
