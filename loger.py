import os, logging
from flask import current_app

def init_log(log_name):
    from logging.handlers import RotatingFileHandler

    log_format = '%(asctime)s [%(levelname)s] in %(module)s: %(message)s'
    log_dir = os.getcwd()+'/log'
    log_file = log_dir +'/'+log_name+'.log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log = logging.getLogger(log_name)
    handler = RotatingFileHandler(log_file, maxBytes=5000000,backupCount=1)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(logging.INFO) #to be changed.
    return log