from pathlib import Path

from loguru import logger


def delete_file(file_path: str):
    # Get the config directory
    CONFIG_DIR = Path(__file__).parent

    # Set file path and create directories if they don't exist
    file_path = Path(CONFIG_DIR / file_path)

    # Check if file exists before deleting
    if file_path.exists():
        file_path.unlink()  # Path's method to delete file
        logger.info(f'Deleted file {file_path}')
    else:
        logger.warning(f'File {file_path} does not exist')
