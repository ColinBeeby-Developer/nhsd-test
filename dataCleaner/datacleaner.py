'''
File contains classes and methods to cleanse data
'''
import json

class DataCleaner(object):
    '''
    Class provides methods which clean data
    '''

    def __init__(self,
                 logger,
                 queryProvider):
        '''
        Constructor
        '''
        self.logger = logger
        self.queryProvider = queryProvider
        
    def cleanData(self,
                  data,
                  logDict):
        '''
        Method to return the provided data, cleansed
        '''
        try:
            dataDict = json.loads(data)
        except ValueError:
            self.logger.log('CLEANER0007',
                            logDict)
            raise ValueError
        
        if not dataDict.get('id'):
            self.logger.log('CLEANER0008',
                            logDict)
            raise ValueError
        
        personPreferences = self.queryProvider.getPersonPreferences(dataDict['id'],
                                                                    logDict)
        logDict['id'] = dataDict['id']
        self.logger.log('CLEANER0004',
                        logDict)
        
        # obfuscate the id if required
        if personPreferences.get('patientPreference', '') == 'OBFUSCATE_ID':
            dataDict['id'] = personPreferences.get('newId', '')
        self.logger.log('CLEANER0005',
                        logDict)
        
        return json.dumps(dataDict)
    