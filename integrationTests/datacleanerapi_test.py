'''
File contains classes and methods for integration testing the dataCleaner API
'''
import unittest

import integrationTests.swaggerClient 
from integrationTests.swaggerClient.rest import ApiException

PERSON_ID_OBFUSCATE = '0001'
PERSON_ID_NO_OBFUSCATE = '0002'
PERSON_ID_ERROR = '0003'


class TestDataCleanerAPI(unittest.TestCase):


    def setUp(self):
        configuration = integrationTests.swaggerClient.Configuration()
        configuration.host = 'http://127.0.0.1:5000'
        self.api_instance = integrationTests.swaggerClient.DefaultApi(integrationTests.swaggerClient.ApiClient(configuration))

    def testDataCleanerGet_obfuscate(self):
        '''
        Test that a GET call to the /cleanse endpoint functions as expected
        The id should be obfuscated in the return
        '''
        # given
        inputData = '{"rowId": 1, "id": "0001", "favouriteColour": "red"}'
        expectedReturn = '{"rowId": 1, "id": "74327ebb14", "favouriteColour": "red"}'
        
        self._postDataAndCheckResult(inputData,
                                     expectedReturn)
        
    def testDataCleanerPost_noObfuscate(self):
        '''
        Test that a POST call to the /cleanse endpoint functions as expected
        The id should not be obfuscated in the return
        '''
        # given
        inputData = '{"rowId": 2, "id": "0002", "favouriteColour": "green"}'
        expectedReturn = '{"rowId": 2, "id": "0002", "favouriteColour": "green"}'
        
        self._postDataAndCheckResult(inputData,
                                     expectedReturn)
        
    def testDataCleanerPost_error(self):
        '''
        Test that a POST call to the /cleanse endpoint functions as expected.
        Ensure that errors are handles gracefully
        '''
        # given
        inputData = '{"rowId": 3, "id": "0003", "favouriteColour": "blue"}'
        expectedReturn = '{"rowId": 3, "id": "0003", "favouriteColour": "blue"}'
        expectedHttpCode = '504'
        
        with self.assertRaises(ApiException) as context:
            self._postDataAndCheckResult(inputData,
                                         expectedReturn,
                                         expectedHttpCode)
        self.assertTrue(context.exception.status,
                        expectedHttpCode)
        
        
        
    def _postDataAndCheckResult(self,
                                inputData,
                                expectedReturn,
                                expectedHttpCode=200):
        '''
        Method to post the input data to the dataCleanerApi and check that
        the response is as expected
        '''
        # when
        actualReturn = self.api_instance.post_data_cleaner_api_with_http_info(inputData)
        
        # then
        self.assertEqual(expectedReturn,
                         actualReturn[0],
                         'Expected value {} and Actual value {} differ'.format(expectedReturn,
                                                                               actualReturn))
        self.assertEqual(expectedHttpCode,
                         actualReturn[1],
                         'Expected HTTP code {} and Actual HTTP code {} differ.'.format(expectedHttpCode,
                                                                                        actualReturn[1]))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataCleanerGet']
    unittest.main()
    