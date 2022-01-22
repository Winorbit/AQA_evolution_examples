import os
import logging  
import logging.config  
import json

from pythonjsonlogger import jsonlogger

HOST = os.environ.get('HOST')
if not HOST:
    HOST = "0.0.0.0"

APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
if not APP_SECRET_KEY:
    raise Exception("Secret key for app not defined")

DB_PATH = os.environ.get('DB_PATH')
if not DB_PATH:
    raise Exception("DB_PATH for app not defined")


logger_settings_filename = "logging_config.json"
current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_logfile = f"{current_dir}/{logger_settings_filename}"

with open(path_to_logfile, 'r') as logger_config:  
    config_dict = json.load(logger_config)  
  
logging.config.dictConfig(config_dict)  
logger = logging.getLogger(__name__)  
logger.info('Logging started')

