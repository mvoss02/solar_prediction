from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the config directory
CONFIG_DIR = Path(__file__).parent


class TrainingConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'training_settings.env'),
        env_file_encoding='utf-8',
    )

    # Feature view with the basic features (NOTE: We will add more features later, which will be more complex and time dependent)
    feature_view_basic_features_name: str = Field(
        description='The name of the feature view with basic features'
    )
    feature_view_basic_features_version: int = Field(
        description='The version of the feature view with basic features'
    )

    # Add time based features
    add_time_based_features: bool = Field(
        default=True,
        description='Whether to add time based features',
    )

    # Label
    label: str = Field(description='Label feature')

    # Hyperparameter tuning
    hyperparameter_tuning: bool = Field(
        default=False,
        description='Should hyperparameter tuning be performed?',
    )

    hyperparameter_tuning_search_trials: Optional[int] = Field(
        default=0,
        description='The number of trials to perform for hyperparameter tuning',
    )
    hyperparameter_tuning_n_splits: Optional[int] = Field(
        default=3,
        description='The number of splits to perform for hyperparameter tuning',
    )

    # Model registry
    model_status: Literal['Development', 'Staging', 'Production'] = Field(
        default='Development',
        description='The status of the model in the model registry',
    )

    # Model name
    model_name: Literal['xgbosst', 'sarima'] = Field(
        description='The name of the model'
    )

    # Add computed fields instead of hard coding values in the settings file
    @computed_field
    def start_date(self) -> str:
        return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    @computed_field
    def end_date(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')


training_config = TrainingConfig()


class HopsworksCredentialsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(CONFIG_DIR / 'hopsworks_credentials.env'),
        env_file_encoding='utf-8',
    )

    api_key: str
    project_name: str


hopsworksCredentialsConfig = HopsworksCredentialsConfig()
