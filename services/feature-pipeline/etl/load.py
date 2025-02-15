import polars as pl
from config.config import hopsworksCredentialsConfig, hopsworksSettingsConfig
from hopsworks_utils import HopsworksFeatureManager
from loguru import logger


def load_data_into_feature_group(
    data: pl.DataFrame,
) -> None:
    """
    Load data into a feature group in the Hopsworks Feature Store

    Args:
        api_key (str): The API key for the Hopsworks project
        project_name (str): The name of the Hopsworks project
        feature_group_name (str): The name of the feature group
        feature_group_version (int): The version of the feature group
        feature_group_primary_keys (list[str]): The primary keys of the feature group
        data (pl.DataFrame): The data to load into the feature group

    Returns:
        None

    Raises:
        Exception: If the data fails to be loaded into the feature group
    """

    logger.info(
        f'Creating HopsworksFeatureGroupManager for feature group {hopsworksSettingsConfig.feature_group_name} version {hopsworksSettingsConfig.feature_group_version}'
    )
    feature_group_manager = HopsworksFeatureManager(
        api_key=hopsworksCredentialsConfig.api_key,
        project_name=hopsworksCredentialsConfig.project_name,
        feature_group_name=hopsworksSettingsConfig.feature_group_name,
        feature_group_version=hopsworksSettingsConfig.feature_group_version,
        feature_group_primary_keys=hopsworksSettingsConfig.feature_group_primary_keys,
        feature_group_description=hopsworksSettingsConfig.feature_group_description,
        feature_group_event_time=hopsworksSettingsConfig.feature_group_event_time,
    )

    logger.info(
        f'Inserting data into feature group {hopsworksSettingsConfig.feature_group_name} version {hopsworksSettingsConfig.feature_group_version}'
    )
    feature_group_manager.insert_data_into_feature_group(data=data)
