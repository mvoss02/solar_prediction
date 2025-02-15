from typing import Optional

import polars as pl
from loguru import logger


def _convert_date(
    df: pl.DataFrame, column_name: Optional[str] = 'date'
) -> pl.DataFrame:
    return df.select(
        pl.coalesce(
            pl.col(column_name).str.strptime(pl.Date, '%F', strict=False),
            pl.col(column_name).str.strptime(pl.Date, '%F %T', strict=False),
            pl.col(column_name).str.strptime(pl.Date, '%D', strict=False),
            pl.col(column_name).str.strptime(pl.Date, '%c', strict=False),
        ).alias(column_name)
    )


def _round_all_columns(df: pl.DataFrame, decimal_points: int = 2) -> pl.DataFrame:
    numeric_cols = [
        col for col in df.columns if df.schema[col] in [pl.Float32, pl.Float64]
    ]

    return df.with_columns([pl.col(col).round(decimal_points) for col in numeric_cols])


def _add_label_column(
    df: pl.DataFrame, column_name: str, shift: int = 1
) -> pl.DataFrame:
    return df.with_columns(
        pl.col(column_name).shift(shift).alias(f'{column_name}_label')
    )


def transform_data(df: pl.DataFrame) -> pl.DataFrame:
    logger.info('Converting the date column to a date type.')
    df = df.with_columns(_convert_date(df, 'date').get_column('date'))

    logger.info('Rounding all the columns to a given decimal points.')
    df = _round_all_columns(df, decimal_points=0)

    logger.info(
        "Adding a label column. The label column is the value of 'tsun' the following day."
    )
    df = _add_label_column(df, column_name='tsun', shift=1).drop_nulls().sort('date')

    logger.info('Successfully transformed the data.')

    return df
