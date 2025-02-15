from datetime import datetime, timedelta
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the config directory
CONFIG_DIR = Path(__file__).parent


class MeteostatCredentialsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'meteostat_credentials.env'),
        env_file_encoding='utf-8',
    )

    api_key: str
    api_host: str


meteostatCredentialsConfig = MeteostatCredentialsConfig()


class MeteostatSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'meteostat_settings.env'),
        env_file_encoding='utf-8',
    )

    meteostat_endpoint: str
    station_id: str
    start_date: str
    end_date: str
    table_name: str
    yaml_config_file: str
    output_path: str

    # Add computed fields instead of hard coding values in the settings file
    @computed_field
    def start_date(self) -> str:
        return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    @computed_field
    def end_date(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')


meteostatSettingsConfig = MeteostatSettingsConfig()


class HopsworksSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'hopsworks_settings.env'),
        env_file_encoding='utf-8',
    )

    feature_group_name: str
    feature_group_version: int
    feature_group_primary_keys: list[str]
    feature_group_description: str
    feature_group_event_time: str


hopsworksSettingsConfig = HopsworksSettingsConfig()


class HopsworksCredentialsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'hopsworks_credentials.env'),
        env_file_encoding='utf-8',
    )

    api_key: str
    project_name: str


hopsworksCredentialsConfig = HopsworksCredentialsConfig()
