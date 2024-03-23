import os
from datetime import datetime

DATABASE_NAME = 'DB_NAME'
COLLECTION_NAME = 'visa_data'
MONGODB_URL_KEY = "mongodb+srv://Annied:6guru_balaji@cluster0.lpr7jl3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME: str = 'model.pkl'

TARGET_COLUMN = 'case_status'

FILE_NAME: str = "usvisa.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("config","schema.yaml")

"""
Data Ingestion related constants will start from DATA_INGESTION_VAR_NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constants will start from DATA_VALIDATION_VAR_NAME
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

