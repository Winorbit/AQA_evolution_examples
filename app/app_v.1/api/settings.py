# import dotenv
import os
import logging  
import logging.config  
import json
from pythonjsonlogger import jsonlogger

logger_settings_filename = "logging_config.json"
current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_logfile = f"{current_dir}/{logger_settings_filename}"

with open(path_to_logfile, 'r') as logger_config:  
    config_dict = json.load(logger_config)  
  
logging.config.dictConfig(config_dict)  
logger = logging.getLogger(__name__)  
logger.info('Logging started')

