import json
import os, sys
import pandas as pd
from us_visa.constant import *
from us_visa.logger import logging
from evidently.model_profile import Profile
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from evidently.model_profile.sections import DataDriftProfileSection
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact
        :param data_validation_config
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise USvisaException(e, sys)

    def validate_number_of_columns(self, df):
        try:
            status = len(df.columns) == len(self._schema_config['columns'])
            logging.info(f"Is required columns present: [{status}]")
            return status

        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df):
        """
        Method Name: validate_number_of_columns
        Description: It tell validates the number of columns
        Output: Returns a bool value
        On Failure: Write an exception log and raise the error
        """
        try:
            df_columns1 = df.columns
            missing_numerical_column = []
            missing_categorical_column = []
            for column in self._schema_config['numerical_columns']:
                if column not in df_columns1:
                    missing_numerical_column.append(column)
            if len(missing_numerical_column) > 0:
                logging.info(f"Missing Numerical columns {missing_numerical_column}")

            for column in self._schema_config['categorical_columns']:
                if column not in df_columns1:
                    missing_categorical_column.append(column)
            if len(missing_numerical_column) > 0:
                logging.info(f"Missing Numerical columns {missing_categorical_column}")

            return False if len(missing_numerical_column) > 0 or len(missing_categorical_column) > 0 else True

        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(filepath):
        try:
            return pd.read_csv(filepath)

        except Exception as e:
            raise USvisaException(e, sys)

    def detect_data_drift(self, referrence_dataframe, current_dataframe):
        """
        This method will give us a report on datadrift, will return a bool value
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(referrence_dataframe, current_dataframe)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

            return drift_status

        except Exception as e:
            raise USvisaException(e, sys)

    def inititate_data_validation(self):
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline

        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            validation_error_message = ""
            logging.info("Starting Data Validation")
            traindf = DataValidation.read_data(filepath=self.data_ingestion_artifact.trained_file_path)
            testdf = DataValidation.read_data(filepath=self.data_ingestion_artifact.test_file_path)

            status = self.validate_number_of_columns(traindf)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_message += f"Columns are missing in training dataframe."

            status = self.validate_number_of_columns(testdf)
            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_message += f"Columns are missing in test dataframe."

            status = self.is_column_exist(df=traindf)

            if not status:
                validation_error_message += f"Columns are missing in training dataframe."

            status = self.is_column_exist(df=testdf)
            if not status:
                validation_error_message += f"columns are missing in test dataframe."

            validation_status = len(validation_error_message) == 0

            if validation_status:
                drift_status = self.detect_data_drift(traindf, testdf)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_message = "Drift detected"
                else:
                    validation_error_message = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_message}")

            data_validation_artifact = DataValidationArtifact(validation_status=validation_status,
                                                              message=validation_error_message,
                                                              drift_report_file_path=self.data_validation_config.drift_report_file_path)

            return data_validation_artifact

        except Exception as e:
            raise USvisaException(e, sys)
