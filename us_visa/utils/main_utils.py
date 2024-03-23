import dill
import yaml
import os, sys
import numpy as np
import pandas as pd
from us_visa.logger import logging
from us_visa.exception import USvisaException


def read_data(filepath):
    return pd.DataFrame(filepath)


def read_yaml_file(file_path):
    """
    This function will read the yaml file
    :param file_path: yaml file path
    :return: dict
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise USvisaException(e, sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False):
    """
    In this function if the replace value is True then it will write in the yaml file
    :param replace:
    :param content:
    :param file_path, content, replace
    :return: None
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(content, yaml_file)

    except Exception as e:
        raise USvisaException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj1:
            np.save(file_obj1, array)
    except Exception as e:
        raise USvisaException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise USvisaException(e, sys)


def drop_columns(df, cols: list) -> DataFrame:
    """
    drop the columns form a pandas DataFrame
    df: pandas DataFrame
    cols: list of columns to be dropped
    """
    logging.info("Entered drop_columns methon of utils")

    try:
        df = df.drop(columns=cols, axis=1)

        logging.info("Exited the drop_columns method of utils")

        return df
    except Exception as e:
        raise USvisaException(e, sys)