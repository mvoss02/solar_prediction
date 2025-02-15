import hopsworks
import polars as pl
from hsfs.feature_view import FeatureView
from loguru import logger


class HopsworksFeatureGroupManager:
    """
    A class to manage feature groups and feature views in the Hopsworks Feature Store
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_description: str,
        feature_group_event_time: str,
    ):
        """
        Establish a connection to the Hopsworks Feature Store and set up the feature group
        """
        self.feature_group_name = feature_group_name
        self.feature_group_version = feature_group_version

        # Establish a connection to the Hopsworks Feature Store
        logger.info(f'Logging in to Hopsworks project {project_name}')
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._feature_store = project.get_feature_store()

        # Get the feature group
        logger.info(
            f'Getting or creating feature group {feature_group_name} version {feature_group_version}'
        )
        self._feature_group = self._feature_store.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            description=feature_group_description,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=False,
            statistics_config={
                'enabled': True,
                'histograms': True,
                'correlations': True,
            },
            time_travel_format='DATE',
        )
        logger.info(
            f'Successfully connected to feature group {feature_group_name} version {feature_group_version}'
        )

    def insert_data_into_feature_group(self, data: pl.DataFrame) -> None:
        """
        Insert data into a feature group

        Args:
            data (pl.DataFrame): The data to insert into the feature group

        Returns:
            None

        Raises:
            Exception: If the data fails to be inserted into the feature group

        """
        try:
            # Convert Polars DataFrame to Pandas DataFrame
            pandas_df = data.to_pandas()

            # Convert timestamp to date if needed
            pandas_df['date'] = pandas_df['date'].dt.date

            # Insert data into the feature group
            self._feature_group.insert(
                pandas_df,
                write_options={
                    'wait_for_job': True,
                    'overwrite': False,
                },
            )
            logger.info(
                f'Successfully inserted data into feature group {self.feature_group_name}'
            )

            # Add feature descriptions and statistics
            logger.info(
                f'Updating feature descriptions and statistics for feature group {self.feature_group_name}'
            )
            feature_descriptions = [
                {
                    'name': 'date',
                    'description': """
                                    The date of the data point.
                                    """,
                    'validation_rules': 'date',
                },
                {
                    'name': 'tavg',
                    'description': """
                                    Average temperature in degrees Celsius.
                                    """,
                    'validation_rules': '>=-20 and <=40 (float)',
                },
                {
                    'name': 'tmin',
                    'description': """
                                    Minimum temperature in degrees Celsius.
                                    """,
                    'validation_rules': '>=-20 and <=40 (float)',
                },
                {
                    'name': 'tmax',
                    'description': """
                                    Maximum temperature in degrees Celsius.
                                    """,
                    'validation_rules': '>=-20 and <=40 (float)',
                },
                {
                    'name': 'prcp',
                    'description': """
                                    The daily precipitation total in mm.
                                    """,
                    'validation_rules': '>=0 and <=1000 (float)',
                },
                {
                    'name': 'snow',
                    'description': """
                                    The snow depth in mm.
                                    """,
                    'validation_rules': '>=0 and <=100 (float)',
                },
                {
                    'name': 'wdir',
                    'description': """
                                    The average wind direction in degrees (°).
                                    """,
                    'validation_rules': '>=0 and <=360 (float)',
                },
                {
                    'name': 'wspd',
                    'description': """
                                    The average wind speed in km/h.
                                    """,
                    'validation_rules': '>=0 and <=100 (float)',
                },
                {
                    'name': 'wpgt',
                    'description': """
                                    The peak wind gust in km/h.
                                    """,
                    'validation_rules': '>=0 and <=100 (float)',
                },
                {
                    'name': 'pres',
                    'description': """
                                    The average sea-level air pressure in hPa.
                                    """,
                    'validation_rules': '>=900 and <=1100 (float)',
                },
                {
                    'name': 'tsun',
                    'description': """
                                    The daily sunshine total in minutes (m).
                                    """,
                    'validation_rules': '>=0 and <=1440 (float)',
                },
                {
                    'name': 'tsun_label',
                    'description': """
                                    The daily sunshine total in minutes (m) as a label, shifted by 1 day.
                                    """,
                    'validation_rules': '>=0 and <=1440 (float)',
                },
            ]

            for description in feature_descriptions:
                self._feature_group.update_feature_description(
                    description['name'], description['description']
                )

            logger.info(
                f'Successfully updated feature descriptions for feature group {self.feature_group_name}'
            )
        except:
            logger.error(
                f'Failed to insert data into feature group {self.feature_group_name}'
            )
            raise


class HopsworksFeatureViewManager:
    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_view_name: str,
        start_datetime: str,
        end_datetime: str,
    ):
        """
        Establish a connection to the Hopsworks Feature Store and set up the feature view
        """
        self._feature_group_name = feature_group_name
        self._feature_group_version = feature_group_version
        self._feature_view_name = feature_view_name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

        # Establish a connection to the Hopsworks Feature Store
        logger.info(f'Logging in to Hopsworks project {project_name}')
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        self._feature_store = project.get_feature_store()
        self._feature_group = self._feature_store.get_feature_group(
            self._feature_group_name, self._feature_group_version
        )

    def create_feature_view(self, query: str = None) -> FeatureView:
        """
        Create a feature view in the Hopsworks Feature Store

        Args:
            feature_view_name (str): The name of the feature view
            query (str): The SQL query to generate the feature view

        Returns:
            None

        Raises:
            Exception: If the feature view fails to be created

        """
        try:
            # If no query is provided, select all columns from the feature group
            query = self._feature_group.select_all()

            # Create the feature view
            feature_view = self._feature_store.create_feature_view(
                name=self._feature_view_name,
                description=f'Feature view for {self._feature_group_name}',
                query=query,
            )
            logger.info(f'Successfully created feature view {self._feature_view_name}')

            return feature_view
        except:
            logger.error(f'Failed to create feature view {self._feature_view_name}')
            raise

    def get_feature_view(self) -> FeatureView:
        """
        Get a feature view from the Hopsworks Feature Store

        Args:
            feature_view_name (str): The name of the feature view

        Returns:
            None

        Raises:
            Exception: If the feature view fails to be retrieved

        """
        try:
            # Get the feature view
            feature_view = self._feature_store.get_feature_view(self._feature_view_name)
            logger.info(
                f'Successfully retrieved feature view {self._feature_view_name}'
            )

            return feature_view
        except Exception:
            logger.error(f'Failed to retrieve feature view {self._feature_view_name}')
            raise
