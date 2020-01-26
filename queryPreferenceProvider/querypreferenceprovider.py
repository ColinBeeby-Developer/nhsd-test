'''
File contains classes and methods to interact with the PreferenceProvider API
'''
import ast
import json

from queryPreferenceProvider.swaggerClient import Configuration, DefaultApi, ApiClient
from queryPreferenceProvider.swaggerClient.rest import ApiException

class QueryPreferenceProvider(object):
    '''
    Class provides methods which can be used to query the PreferenceProvider API
    '''

    MAX_ATTEMPTS = 3
    
    def __init__(self,
                 logger,
                 baseUrl='https://preferenceprovider.herokuapp.com'):
        '''
        Constructor
        '''
        self.logger = logger
        configuration = Configuration()
        configuration.host = baseUrl
        self.api_instance = DefaultApi(ApiClient(configuration))
        
    def getPersonPreferences(self,
                             personId,
                             logDict):
        '''
        Return the preferences for the given personId
        '''       
        personPreferences = None
        for attempt in range(self.MAX_ATTEMPTS):
            try:
                logDict['attempt'] = attempt
                self.logger.log('CLEANER0009',
                                logDict)
                personPreferences = self.api_instance.get_preferences(personId)
                break
            except ApiException:
                if attempt > 1:
                    self.logger.log('CLEANER0011',
                                    logDict)
                    raise ApiException()
                continue
            
        return self._processReturnValue(personPreferences,
                                        logDict)
            
    def _processReturnValue(self,
                            personPreferences,
                            logDict):
        '''
        Process the returned person preferences into a return value
        '''
        self.logger.log('CLEANER0010',
                        logDict)
        try:
            retVal = json.loads(json.dumps(ast.literal_eval(personPreferences)))
        except (ValueError, SyntaxError):
            self.logger.log('CLEANER0012',
                            logDict)
            retVal = json.loads('{"patientPreference": "NONE", "newId": null}')
        return retVal
            
        