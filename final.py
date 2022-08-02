import operation 
import multiprocessing
import configparser
import os
import logging

config = configparser.ConfigParser()
config.read(os.path.expanduser('./auth.ini'))

Email = config['AUTH']['EMAIL']
Password = config['AUTH']['PASSWORD']

#use freezin to make the program not run in the background
multiprocessing.freeze_support()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',filename=os.environ["USERPROFILE"] + "\\Documents\\Unscaffold\\logger\\log.log", filemode='w')
logging.info("Starting operation")
start_operation = Operation( Email, Password)
logging.info("Starting process")
start_operation.start()
