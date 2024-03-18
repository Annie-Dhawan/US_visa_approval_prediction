import os
import sys
import numpy as np
import pandas as pd
from typing import Optional
from us_visa.logger import logging
from us_visa.constant import DATABASE_NAME
from us_visa.exception import USvisaException
from us_visa.configuration.mongo_db_connection import MongoDBClient


class USvisaData():
    """
        This class help to export entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            #connecting with db
            self.mongoclient = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e, sys)

    def export_collection_as_dataframe(self, collection_name, database_name: Optional[str] = None):

        try:
            """
                export entire collection as dataframe:
                return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise USvisaException(e, sys)

