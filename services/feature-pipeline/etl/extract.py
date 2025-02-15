import json
from pathlib import Path
from typing import Optional

import polars as pl
import requests
from config.config import meteostatCredentialsConfig, meteostatSettingsConfig
from loguru import logger

from etl.table_config.raw_table_config import RawTableConfig


def extract_data_from_api() -> Optional[pl.DataFrame]:
    """
    Helper function to extract data from the Meteostat API.

    Returns:
        None
    """

    # Get the config directory
    CONFIG_DIR = Path(__file__).parent

    # Set file path and create directories if they don't exist
    file_path = Path(CONFIG_DIR / meteostatSettingsConfig.output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories

    logger.info('Extracting data.')

    # Config for the Meteostat API
    url = meteostatSettingsConfig.meteostat_endpoint
    headers = {
        'x-rapidapi-key': meteostatCredentialsConfig.api_key,
        'x-rapidapi-host': meteostatCredentialsConfig.api_host,
    }
    querystring = {
        'station': meteostatSettingsConfig.station_id,
        'start': meteostatSettingsConfig.start_date,
        'end': meteostatSettingsConfig.end_date,
    }

    if not file_path.exists():
        # Getting the response
        try:
            logger.info(f'Requesting data from API from the following URL: {url}.')
            response = requests.request('GET', url, headers=headers, params=querystring)
        except requests.exceptions.HTTPError as err:
            logger.error(f'HTTP error occurred: {err}.')
            return None

        if response.status_code != 200:
            raise ValueError(
                f'Response status = {response.status_code}. Could not download the data from Meteostat API.'
            )

        logger.info('Data successfully downloaded.')

        # Converting response object to Polars DataFrame
        try:
            logger.info('Store the data in a file.')
            # Write JSON response data
            with file_path.open('w') as f:
                data = json.loads(response.text)

                # Ensure 'data' is written as a JSON string
                json.dump(data['data'], f, indent=4)

            logger.info('Converting response to Polars DataFrame.')
            data = json.loads(response.text)

            # Get polars schema
            table_schema = RawTableConfig(
                meteostatSettingsConfig.yaml_config_file
            ).get_schema(meteostatSettingsConfig.table_name)
            df = pl.DataFrame(data['data'], schema=table_schema)
            return df
        except Exception as e:
            logger.error(
                f'Error occurred while converting response to Polars DataFrame: {e}.'
            )
            return None
    else:
        logger.info(f'File already exists at {file_path}.')
        logger.info(f'Reading the data from the file output path: {file_path}.')
        # Get polars schema
        table_schema = RawTableConfig(
            meteostatSettingsConfig.yaml_config_file
        ).get_schema(meteostatSettingsConfig.table_name)
        df = pl.read_json(file_path, schema=table_schema)
        return df
