import logging

def init_custom():
    format_str = '%(levelname)s - %(name)s\n%(message)s\n%(pathname)s - %(lineno)s\n'

    # Root logger
    logging.basicConfig(level=logging.DEBUG, format=format_str)

    # Console logger
    formatter = logging.Formatter(format_str)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    log = logging.getLogger('rag_debug')
    log.setLevel(logging.DEBUG)
    log.addHandler(console_handler)

    return log

logger = init_custom()

__all__ = ['logger']