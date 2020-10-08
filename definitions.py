import os
import logging
import socket
from datetime import datetime
from logging.handlers import RotatingFileHandler
from enum import Enum

"""Common definitions of methods used throughout the application."""

# Define settings for ALL hl7-related configurations.
HL7_SETTINGS = 'hl7_settings'
PRIOR_AUTH_SETTINGS = 'prior_auth_settings'


class Settings(Enum):
    HL7_SETTINGS = 'hl7_settings'
    PRIOR_AUTH_SETTINGS = 'prior_auth_settings'


def get_project_root() -> str:
    """This file should always be in the root directory.  That way the root directory can always be determined."""
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Project Root
    return root_dir


def setup_logger(logger_name: str, level=logging.WARNING, ext: str = 'log', fh_type: str = 'rotate',
                 show_in_console: bool = True) -> logging:
    """Set up the standard logging file along with constraints such as format, file size, etc."""
    # set up logging to file - see previous section for more details
    logger_name = 'main' if logger_name == '__main__' else logger_name
    log_file_name = f'{get_project_root()}/logs/pid-{os.getpid()}_{logger_name}.{ext}'
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s line %(lineno)d  %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        filename=log_file_name,
                        filemode='a')
    if fh_type == 'rotate':
        handler = RotatingFileHandler(log_file_name, maxBytes=10 * 1024 * 1024, backupCount=5)
    elif fh_type == 'by_date':
        handler = logging.FileHandler(
            '{}/{}-{:%Y-%m-%d}.{}'.format(get_project_root(), logger_name, datetime.now(), ext))
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
    else:
        handler = RotatingFileHandler(log_file_name, maxBytes=10 * 1024 * 1024, backupCount=5)

    my_logger = logging.getLogger(logger_name)
    my_logger.setLevel(level)
    my_logger.addHandler(handler)

    if show_in_console:
        # simple console format
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        my_logger.addHandler(console)
    return my_logger


current_logger = setup_logger(__name__, logging.INFO)


def get_ip_address() -> str:
    """Get the ip address of the platform and check it against a list of values that should not be overridden."""
    ip_address = socket.gethostbyname(socket.gethostname())
    current_logger.info('IP Address {}.'.format(ip_address))
    if ip_address not in ['10.201.144.167', '10.48.164.198', '10.50.8.130']:
        local_host = '127.0.0.1'
        current_logger.info('Replacing {} with {}'.format(ip_address, local_host))
        ip_address = local_host
    current_logger.info('Running on server {}.'.format(ip_address))

    return ip_address


if __name__ == "__main__":
    current_logger = setup_logger(__name__, logging.INFO)
    current_logger.info('sample info')
    current_logger.warning('sample warning')

    print(get_project_root())
    print(get_ip_address())
