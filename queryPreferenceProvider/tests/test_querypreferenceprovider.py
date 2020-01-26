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

class MockQueryPreferenceProvider(QueryPreferenceProvider):
    '''
    Mock QueryPreferenceProvider class
    Bypasses initialization
    '''
    
    def __init__(self):
        self.logger = MockLogger()
    


class TestQueryPreferenceProvider(unittest.TestCase):
    '''
    Class containing tests for QueryPreferenceProvider
    '''
        
    def testProcessReturnValue(self):
        '''
        Test that the _processReturnValue method gives the corrent answer
        '''
        # given
        expectedValue = json.loads('{"patientPreference": "NONE", "newId": null}')
        
        # when
        mockQueryPreferenceProvider = MockQueryPreferenceProvider()
        actualValue = mockQueryPreferenceProvider._processReturnValue('NOT JSON',
                                                                      {})
        
        # then
        self.assertEqual(expectedValue,
                         actualValue,
                         'Return value from _processReturnValue is not as expected')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetPersonPreferences']
    unittest.main()