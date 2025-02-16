from typing import Optional

import numpy as np
import optuna
import polars as pl
from loguru import logger
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor


class XGBoostModel:
    """
    Encapsulates the training logic with or without hyperparameter tuning, depending on
    settings using an XGBRegressor.
    """

    def __init__(self):
        self.model = XGBRegressor(
            objective='reg:absoluteerror',
            eval_metric=['mae'],
        )

    def get_model_object(self):
        """
        Returns the model object.
        """
        return self.model

    def fit(
        self,
        X: pl.DataFrame,
        y: pl.Series,
        n_search_trials: Optional[int] = 0,
        n_splits: Optional[int] = 3,
        hyperparameter_tuning: bool = False,
    ):
        """
        Fits the an XGBoostRegressor model to the training data, either with or without
        hyperparameter tuning.

        Args:
            X (pl.DataFrame): The training data (independent features)
            y (pl.Series): The target variable (label)
            hyperparameter_tuning (bool): Whether to perform hyperparameter tuning or not
        """
        if not hyperparameter_tuning:
            logger.info('Fitting XGBoost model without hyperparameter tuning')
            self.model = XGBRegressor()

        else:
            logger.info('Fitting XGBoost model with hyperparameter tuning')

            # Perform hyperparameter tuning with n_search_trials and n_splits
            # and we search for the best hyperparameters using Bayesian optimization
            best_hyperparams = self._find_best_hyperparams(
                X, y, n_search_trials=n_search_trials, n_splits=n_splits
            )
            logger.info(f'Best hyperparameters: {best_hyperparams}')

            # Train model with the best set of hyperparameters
            self.model = XGBRegressor(**best_hyperparams)

        # Train the model
        self.model.fit(X, y)

    def predict(self, X: pl.DataFrame) -> pl.Series:
        # Simple predict method (comes with XGBRegressor)
        return self.model.predict(X)

    def _find_best_hyperparams(
        self,
        X_train: pl.DataFrame,
        y_train: pl.Series,
        n_search_trials: int,
        n_splits: int,
    ) -> dict:
        """
        Finds the best hyperparameters for the model using Bayesian optimization.

        Args:
            X_train: pl.DataFrame, the training data
            y_train: pl.Series, the target variable
            n_search_trials: int, the number of trials to run
            n_splits: int, the number of splits to use for time-based cross-validation

        Returns:
            dict, the best hyperparameters
        """

        def objective(trial: optuna.Trial) -> float:
            """
            Objective function for Optuna that returns the mean absolute error we
            want to minimize.

            Args:
                trial: optuna.Trial, the trial object

            Returns:
                float, the mean absolute error
            """
            # Use Optuna to search for the best hyperparameters
            params = {
                'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
                'max_depth': trial.suggest_int('max_depth', 3, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
                # NOTE: there is totally room for improving the search space
                # Find the complete list of hyperparameters here:
                # https://xgboost.readthedocs.io/en/stable/parameter.html
            }

            # Time-based cross-validation, since we are dealing with time series data (BE CAREFUL: POTENIAL DATA LEAKAGE)
            tscv = TimeSeriesSplit(n_splits=n_splits)
            mae_scores = []
            for train_index, val_index in tscv.split(X_train):
                # split the data into training and validation sets
                X_train_fold, X_val_fold = (
                    X_train.iloc[train_index],
                    X_train.iloc[val_index],
                )
                y_train_fold, y_val_fold = (
                    y_train.iloc[train_index],
                    y_train.iloc[val_index],
                )

                # train the model on the training set
                model = XGBRegressor(**params)
                model.fit(X_train_fold, y_train_fold)

                # evaluate the model on the validation set
                y_pred = model.predict(X_val_fold)
                mae = mean_absolute_error(y_val_fold, y_pred)
                mae_scores.append(mae)

            # Return average MAE
            return np.mean(mae_scores)

        # Create a study object that minimizes the objective function
        study = optuna.create_study(direction='minimize')

        # Run trials = optimize the objective function
        logger.info(f'Running {n_search_trials} trials')
        study.optimize(objective, n_trials=n_search_trials)

        # Return best set of hyperparameters
        return study.best_trial.params
