import os
import sys
import pymongo
import certifi
from us_visa.logger import logging
from us_visa.exception import USvisaException
from us_visa.constant import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()


class MongoDBClient():
    """
        Class Name :   export_data_into_feature_store
        Description :   This method exports the dataframe from mongodb feature store as dataframe

        Output      :   connection to mongodb database
        On Failure  :   raises an exception
        Args:
            database_name (str): Name of the MongoDB database.
            mongo_db_url (str): URL for connecting to MongoDB.
    """

    def __init__(self, database_name=DATABASE_NAME, mongo_db_url=MONGODB_URL_KEY):

        try:

            self.mongo_db_url = mongo_db_url
            # making the connection
            self.client = pymongo.MongoClient(host=mongo_db_url, tlsCAFile=ca)
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")

        except Exception as e:
            raise USvisaException(e, sys)
