'''
File contains classes and methods to interact with the PreferenceProvider API
'''
import ast
import json

import queryPreferenceProvider.swaggerClient 
from queryPreferenceProvider.swaggerClient.rest import ApiException

class QueryPreferenceProvider(object):
    '''
    Class provides methods which can be used to query the PreferenceProvider API
    '''

    def __init__(self,
                 baseUrl='https://preferenceprovider.herokuapp.com'):
        '''
        Constructor
        '''
        configuration = queryPreferenceProvider.swaggerClient.Configuration()
        configuration.host = baseUrl
        self.api_instance = queryPreferenceProvider.swaggerClient.DefaultApi(queryPreferenceProvider.swaggerClient.ApiClient(configuration))
        
    def getPersonPreferences(self, personId):
        '''
        Return the preferences for the given personId
        '''       
        personPreferences = None
        for n in range(3):
            try:
                personPreferences = self.api_instance.get_preferences(personId)
                break
            except ApiException:
                if n > 1:
                    raise ApiException()
                continue

        return json.loads(json.dumps(ast.literal_eval(personPreferences)))
        