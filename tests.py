# import logging
# # Logging settings
# #logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename='/logs/log.txt', format='%(asctime)s - %(levelname)s - %(message)s',
#                     level=logging.INFO, datefmt='%d-%m-%y %H:%M:%S')
#
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
import fileHandler

uname = input("name")
urole = input("role")

fileHandler.write("test.txt", uname, urole, "0")
