'''
File contains classes and methods to cleanse data
'''
import json
from integrationTests.swaggerClient.rest import ApiException
from flask_restplus import abort

class DataCleaner(object):
    '''
    Class provides methods which clean data
    '''

    def __init__(self, queryProvider):
        '''
        Constructor
        '''
        self.queryProvider = queryProvider
        
    def cleanData(self, data):
        '''
        Method to return the provided data, cleansed
        '''
        try:
            dataDict = json.loads(data)
        except ValueError as e:
            print('need to log this')
            return 'Something when wrong'
        
        # TODO check that the data id is present (and in correct format)
        
        # get the id out of the data
#         try:
        personPreferences = self.queryProvider.getPersonPreferences(dataDict['id'])
#         except ApiException:
#             abort(504, 'Gateway Timeout')
        
        # obfuscate the id if required
        if personPreferences.get('patientPreference', '') == 'OBFUSCATE_ID':
            dataDict['id'] = personPreferences.get('newId', '')
        
        return json.dumps(dataDict)
    