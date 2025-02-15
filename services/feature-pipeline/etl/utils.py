import os

from loguru import logger


def delete_file(file_path: str):
    # Check if file exists before deleting
    if os.path.exists(file_path):
        os.remove(file_path)

        logger.info(f'Deleted file {file_path}')
    else:
        logger.warning(f'File {file_path} does not exist')
