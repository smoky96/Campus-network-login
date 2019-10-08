import logging
import os
import time

import project_root_dir

root_path = os.path.join(project_root_dir.project_dir)
log_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))


def setup_custom_log(logger_path, file_name) -> [logging.Logger, str]:
    """
    :param logger_path: Path relative to project root directory
    :param file_name: logger or logger file name
    :return: logging.Logger
    """

    log_dir = os.path.join(root_path, logger_path, '{}'.format(log_time))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print("log directory: {} created".format(log_dir))
    log_file = os.path.join(log_dir, '{}.log'.format(file_name))

    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger, log_dir
