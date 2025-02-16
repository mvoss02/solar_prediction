import pandas as pd
from loguru import logger


class TimeSeriesFeaturesGenerator:
    """Utility class for generating time-based features for solar data"""

    @staticmethod
    def create_time_features(
        df: pd.DataFrame, datetime_column: str = 'date'
    ) -> pd.DataFrame:
        """
        Create time-based features from a datetime column

        Args:
            df (pd.DataFrame): Input DataFrame with datetime column
            datetime_column (date): Name of the datetime column

        Returns:
            pl.DataFrame: DataFrame with additional time-based features
        """
        try:
            # TODO: Add more time-based features
            # First ensure your date column is set as the index and is datetime type
            df[datetime_column] = pd.to_datetime(df[datetime_column])

            # Create time-based features
            df = df.set_index(datetime_column).sort_index()
            df['tavg_rolling_mean'] = df['tavg'].rolling('7D').mean()
            df = df.reset_index(drop=False)

            return df

        except Exception as e:
            logger.error(f'Error creating time features: {str(e)}')
            raise
