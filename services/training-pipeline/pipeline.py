import pandas as pd
from config.config import hopsworksCredentialsConfig, training_config
from feature_reader import BasicFeatureViewManager
from loguru import logger
from utils.time_series_features import TimeSeriesFeaturesGenerator


def pipeline():
    # Initialize the basic feature view manager
    logger.info('Initializing the basic feature view manager')
    feature_view_manager = BasicFeatureViewManager(
        api_key=hopsworksCredentialsConfig.api_key,
        project_name=hopsworksCredentialsConfig.project_name,
        feature_view_name=training_config.feature_view_basic_features_name,
        feature_view_version=training_config.feature_view_basic_features_version,
        label=training_config.label,
        start_datetime=training_config.start_date,
        end_datetime=training_config.end_date,
    )

    # Get training data
    logger.info('Getting training data')
    training_data = (
        feature_view_manager.get_training_data()
    )  # NOTE: Returns pandas dataframe, hence, we will continue to use it as such
    training_data = pd.DataFrame(training_data)
    logger.info(f'Training data successfully retrieved: {training_data.shape}')

    # Create time-based features if enabled
    if training_config.add_time_based_features:
        logger.info('Creating time-based features')
        training_data = TimeSeriesFeaturesGenerator.create_time_features(training_data)
        logger.info(f'Successfully created time-based features: {training_data.shape}')


if __name__ == '__main__':
    pipeline()
