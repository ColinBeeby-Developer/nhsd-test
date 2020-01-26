'''
This file containt classes and methods to log events to file
'''
from datetime import datetime
import os

class Logger(object):
    '''
    This class implements methods to log events to file
    '''
    LOGPOINT_DICT = {
        'CLEANER0001': 'DataCleaner API POST has been called internalID={internalID}',
        'CLEANER0002': 'DataCleaner API POST has completed internalID={internalID}',
        'CLEANER0003': 'DataCleaner API POST aborting with Gateway Timeout internalID={internalID}',
        'CLEANER0004': 'DataCleaner module has acquired the preferences for {id} internalID={internalID}',
        'CLEANER0005': 'DataCleaner module has performed any required operations for {id} internalID={internalID}',
        'CLEANER0006': 'DataCleaner API POST aborting with Bad Request internalID={internalID}',
        'CLEANER0007': 'DataCleaner module failed to interpret the request data internalID={internalID}',
        'CLEANER0008': 'DataCleaner module failed to find id in request data internalID={internalID}',
        'CLEANER0009': 'DataCleaner Preference Provider attempting to get preferences attempt={attempt} internalID={internalID}',
        'CLEANER0010': 'DataCleaner Preference Provider returning preference data internalID={internalID}',
        'CLEANER0011': 'DataCleaner Preference Provider failed to get preferences internalID={internalID}',
        'CLEANER0012': 'DataCleaner Preference Provider failed to decode preferences internalID={internalID}'
            }

    def __init__(self, file='log.txt'):
        '''
        Constructor
        '''
        self.file = open(file, 'a+')
        
    def log(self, logpoint, dataDict):
        '''
        Add a log message to the log file
        '''
        dateTimeNow = datetime.now().strftime('%Y%m%d %H:%M:%S.%f')
        logpointText = self.LOGPOINT_DICT.get(logpoint, 'logpoint {} not found'.format(logpoint)).format(**dataDict)
        message = '{} - {} - {}'.format(dateTimeNow,
                                        logpoint,
                                        logpointText)
        self.file.write(message + os.linesep)
        