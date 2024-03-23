import dill
import yaml
import os, sys
import numpy as np
import pandas as pd
from us_visa.logger import logging
from us_visa.exception import USvisaException


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
    :param file_path, content, replace
    :return: None
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.dump(content, yaml_file)

    except Exception as e:
        raise USvisaException(e,sys)
