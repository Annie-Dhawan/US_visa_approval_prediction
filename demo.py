import sys
from us_visa.logger import logging
from us_visa.exception import USvisaException




logging.info("Welcome to our Custom log")

try:
    a = 1/"10"
except Exception as e:
    logging.info(e)
