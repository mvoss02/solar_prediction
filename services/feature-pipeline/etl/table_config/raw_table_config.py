from pathlib import Path
from typing import Any, Dict

import polars as pl
import yaml


class RawTableConfig:
    def __init__(self, config_path: str):
        # Get the config directory
        CONFIG_DIR = Path(__file__).parent
        final_config_path = str(CONFIG_DIR / config_path)

        self.config = self._load_config(final_config_path)

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load the configuration file (yaml)"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def get_schema(self, table_name: str) -> Dict[str, type]:
        """Get Pandas schema for a table"""
        type_mapping = {
            'String': pl.String,
            'Int64': pl.Int64,
            'Int32': pl.Int32,
            'Int16': pl.Int16,
            'Float64': pl.Float64,
            'Float32': pl.Float32,
            'Utf8': pl.Utf8,
            'Date': pl.Date,
            'Datetime': pl.Datetime,
            'Boolean': pl.Boolean,
        }

        table_config = self.config[table_name]
        datatypes = table_config['datatypes']

        return {
            col_name: type_mapping[datatypes[col_name]]
            for col_name in table_config['columns']
        }

    def get_columns(self, table_name: str) -> list:
        """Get column names for a table"""
        return list(self.config[table_name]['columns'])


# Usage example:
if __name__ == '__main__':
    # Load configuration
    config = RawTableConfig('raw_data_table_config.yaml')

    # Get schema for a table
    schema = config.get_schema('WeatherData')

    # Use schema with Polars
    df = pl.DataFrame(schema=schema)
