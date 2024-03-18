import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

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

"""
Data Ingestion related constants will start from DATA_INGESTION_VAR_NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DATA: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
