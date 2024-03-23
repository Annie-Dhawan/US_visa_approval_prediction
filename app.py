import os, sys
from us_visa.pipeline.training_pipeline import TrainPipeline
from us_visa.logger import logging


pipeline = TrainPipeline()
pipeline.run_pipeline()
