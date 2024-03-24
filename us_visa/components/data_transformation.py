import yaml
import os, sys
import numpy as np
import pandas as pd
from us_visa.constant import *
from us_visa.logger import logging
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from us_visa.utils.main_utils import *
from us_visa.exception import USvisaException
from sklearn.compose import ColumnTransformer
from us_visa.entity.estimator import TargetValueMapping
from us_visa.entity.config_entity import DataTransformationConfig
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from us_visa.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact, DataTransformationArtifact


class DataTransformation:

    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise USvisaException(e, sys)

    def get_data_transformer_object(self):

        """
        Method Name :   get_data_transformer_object
        Description :   This method creates and returns a data transformer object for the data

        Output      :   data transformer object is created and returned
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )
        try:
            logging.info("Got numerical cols from schema config")
            numeric_transformer = StandardScaler()
            ordinal_encoder = OrdinalEncoder()
            oh_transformer = OneHotEncoder()

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info("Initialize PowerTransformer")

            transform_pipe = Pipeline(steps=[
                ('transform', PowerTransformer(method='yeo-johnson'))
            ])

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, oh_columns),
                    ("Ordinal_Encoder", ordinal_encoder, or_columns),
                    ("Transformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features)
                ]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
            return preprocessor

        except Exception as e:
            raise USvisaException(e, sys)

    def initiate_data_transformation(self):
        """
            Method Name :   initiate_data_transformation
            Description :   This method initiates the data transformation component for the pipeline

            Output      :   data transformer steps are performed and preprocessor object is created
            On Failure  :   Write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting Data Transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info('Got the preprocessor object')

                train_df = read_data(filepath=self.data_ingestion_artifact.trained_file_path)
                test_df = read_data(filepath=self.data_ingestion_artifact.test_file_path)

                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                logging.info("Got the train input features and target features")

                input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
                logging.info("Added company age col")

                drop_cols = self._schema_config['drop_columns']

                logging.info(f'Dropping the cols {drop_cols}')

                input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)

                #target mapping
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )

                #now for testing data
                input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]
                logging.info("Got the test input features and target features")

                input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']
                logging.info('Added company age col in test data')

                logging.info("Dropping the cols from test data")

                input_feature_test_df = drop_columns(df=input_feature_test_df, cols=drop_cols)

                #target mapping
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )

                logging.info("Got train features and test features of Testing dataset")

                logging.info(
                    "Applying preprocessing object on training dataframe and testing dataframe"
                )

                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

                logging.info(
                    "Used the preprocessor object to fit transform the train features"
                )

                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info("Used the preprocessor object to transform the test features")

                logging.info("Applying SMOTEENN on Training dataset")

                smt = SMOTEENN(sampling_strategy="minority")

                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr, target_feature_train_df
                )

                logging.info("Applied SMOTEENN on training dataset")

                logging.info("Applying SMOTEENN on testing dataset")

                input_feature_test_final, target_feature_test_final = smt.fit_resample(
                    input_feature_test_arr, target_feature_test_df
                )

                logging.info("Applied SMOTEENN on testing dataset")

                logging.info("Created train array and test array")

                train_arr = np.c_[
                    input_feature_train_final, np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                    input_feature_test_final, np.array(target_feature_test_final)
                ]

                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)

                logging.info("Saved the preprocessor object")

                logging.info(
                    "Exited initiate_data_transformation method of Data_Transformation class"
                )

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                return data_transformation_artifact

        except Exception as e:
            raise USvisaException(e,sys)
