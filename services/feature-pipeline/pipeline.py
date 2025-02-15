from config.config import meteostatSettingsConfig
from etl import extract, load, transform
from etl.utils import delete_file
from loguru import logger


def pipeline():
    """
    The main function that orchestrates the feature pipeline.
    """

    logger.info('Starting the feature pipeline.')
    logger.info('Extracting data from the Meteostat API.')
    extarcted_data = extract.extract_data_from_api()

    logger.info('Transforming the extracted data.')
    transformed_data = transform.transform_data(df=extarcted_data)

    logger.info('Loading the transformed data into the Feature Store.')
    load.load_data_into_feature_group(data=transformed_data)

    logger.info('Deleting the extracted data file.')
    delete_file(file_path=meteostatSettingsConfig.output_path)

    logger.info('Successfully completed the feature pipeline.')


if __name__ == '__main__':
    pipeline()
