'''
This file contains tests for the querypreferenceprovider module
'''
import json
import unittest

from queryPreferenceProvider.querypreferenceprovider import QueryPreferenceProvider

class MockLogger(object):
    '''
    Mock logger class
    Just provides the method calls
    '''
    def log(self,
            logPoint,
            logDict):
        '''
        Mock log method - does nothing
        '''
        pass
    
class MockAPIInstance(object):
    '''
    Mock API instance class
    Just provides the method calls
    '''
    def get_preferences(self, _):
        '''
        Mock get_preferences method
        return invalid JSON
        '''
        return 'NOT JSON'

class MockQueryPreferenceProvider(QueryPreferenceProvider):
    '''
    Mock QueryPreferenceProvider class
    Bypasses initialization
    '''
    
    def __init__(self):
        self.logger = MockLogger()
        self.api_instance = MockAPIInstance()
    


class TestQueryPreferenceProvider(unittest.TestCase):
    '''
    Class containing tests for QueryPreferenceProvider
    '''

    def testGetPersonPreferences(self):
        '''
        Test that the getPersonPreferences method gives the correct answer
        when invalid json is returned from the PreferenceProvider API
        '''
        # given
        expectedValue = json.loads('{"patientPreference": "NONE", "newId": null}')
        
        # when
        mockQueryPreferenceProvider = MockQueryPreferenceProvider()
        actualValue = mockQueryPreferenceProvider.getPersonPreferences('0099', {})
        
        # then
        self.assertEqual(expectedValue,
                         actualValue,
                         'Return value from getPersonPreferences is not as expected')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetPersonPreferences']
    unittest.main()