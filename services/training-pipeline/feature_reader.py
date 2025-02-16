from typing import Optional

import hopsworks
import pandas as pd
from hsfs.feature_view import FeatureView
from loguru import logger


class BasicFeatureViewManager:
    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_view_name: str,
        feature_view_version: int,
        label: str,
        start_datetime: Optional[str] = None,
        end_datetime: Optional[str] = None,
    ):
        """
        Initialize the basic feature view manager

        Args:
            api_key (str): Hopsworks API key
            project_name (str): Name of the Hopsworks project
            feature_view_name (str): Name of the basic feature view
            feature_view_version (int): Version of the feature view
            label (str): Name of the label column
            start_datetime (Optional[str]): Start date for training data
            end_datetime (Optional[str]): End date for training data
        """
        self._feature_view_name = feature_view_name
        self._feature_view_version = feature_view_version
        self._label = label
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

        # Connect to Hopsworks
        logger.info(f'Logging in to Hopsworks project {project_name}')
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._feature_store = project.get_feature_store()

    def _get_feature_view(self) -> FeatureView:
        """
        Get the basic feature view

        Returns:
            FeatureView: The basic feature view

        Raises:
            Exception: If feature view cannot be retrieved
        """
        try:
            feature_view = self._feature_store.get_feature_view(
                name=self._feature_view_name, version=self._feature_view_version
            )
            logger.info(f'Retrieved feature view {self._feature_view_name}')
            return feature_view

        except Exception as e:
            logger.error(
                f'Error retrieving feature view {self._feature_view_name}: {str(e)}'
            )
            raise

    def get_training_data(self) -> pd.DataFrame:
        """
        Get training data from the feature view

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: X (features) and y (labels)

        Raises:
            Exception: If training data cannot be retrieved
        """
        try:
            feature_view = self._get_feature_view()

            training_data, _ = feature_view.training_data(
                start_time=self.start_datetime,
                end_time=self.end_datetime,
                label=self._label,
            )

            return training_data

        except Exception as e:
            logger.error(f'Error getting training data: {str(e)}')
            raise
