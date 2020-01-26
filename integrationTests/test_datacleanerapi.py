'''
File contains classes and methods for integration testing the dataCleaner API
'''
import unittest

import integrationTests.swaggerClient 
from integrationTests.swaggerClient.rest import ApiException

LOG_POINT_1 = 'CLEANER0001 - DataCleaner API POST has been called internalID='
LOG_POINT_2 = 'CLEANER0002 - DataCleaner API POST has completed internalID='
LOG_POINT_3 = 'CLEANER0003 - DataCleaner API POST aborting with Gateway Timeout internalID='
LOG_POINT_4 = 'CLEANER0004 - DataCleaner module has acquired the preferences for {} internalID='
LOG_POINT_5 = 'CLEANER0005 - DataCleaner module has performed any required operations for {} internalID='
LOG_POINT_6 = 'CLEANER0006 - DataCleaner API POST aborting with Bad Request internalID='
LOG_POINT_7 = 'CLEANER0007 - DataCleaner module failed to interpret the request data internalID='
LOG_POINT_9 = 'CLEANER0009 - DataCleaner Preference Provider attempting to get preferences attempt={} internalID='
LOG_POINT_10 = 'CLEANER0010 - DataCleaner Preference Provider returning preference data internalID='
LOG_POINT_11 = 'CLEANER0011 - DataCleaner Preference Provider failed to get preferences internalID='


class TestDataCleanerAPI(unittest.TestCase):


    def setUp(self):
        configuration = integrationTests.swaggerClient.Configuration()
        configuration.host = 'http://127.0.0.1:5000'
        self.api_instance = integrationTests.swaggerClient.DefaultApi(integrationTests.swaggerClient.ApiClient(configuration))
        self.logFile = open('/tmp/log.txt', 'a+')
    
    def tearDown(self):
        self.logFile.close()

    def testDataCleanerPost_obfuscate(self):
        '''
        Test that a GET call to the /cleanse endpoint functions as expected
        The id should be obfuscated in the return
        '''
        inputData = '{"rowId": 1, "id": "0001", "favouriteColour": "red"}'
        expectedReturn = '{"rowId": 1, "id": "74327ebb14", "favouriteColour": "red"}'
        messagesToFind = [LOG_POINT_1,
                          LOG_POINT_2,
                          LOG_POINT_4.format('0001'),
                          LOG_POINT_5.format('0001'),
                          LOG_POINT_9.format('0'),
                          LOG_POINT_10]
        
        self._postDataAndCheckResult(inputData,
                                     expectedReturn,
                                     messagesToFind=messagesToFind)
        
    def testDataCleanerPost_noObfuscate(self):
        '''
        Test that a POST call to the /cleanse endpoint functions as expected
        The id should not be obfuscated in the return
        '''
        inputData = '{"rowId": 2, "id": "0002", "favouriteColour": "green"}'
        expectedReturn = '{"rowId": 2, "id": "0002", "favouriteColour": "green"}'
        messagesToFind = [LOG_POINT_1,
                          LOG_POINT_2,
                          LOG_POINT_4.format('0002'),
                          LOG_POINT_5.format('0002'),
                          LOG_POINT_9.format('0'),
                          LOG_POINT_10]
        
        self._postDataAndCheckResult(inputData,
                                     expectedReturn,
                                     messagesToFind=messagesToFind)
        
    def testDataCleanerPost_error(self):
        '''
        Test that a POST call to the /cleanse endpoint functions as expected.
        Ensure that errors are handles gracefully
        '''
        # given
        inputData = '{"rowId": 3, "id": "0003", "favouriteColour": "blue"}'
        expectedReturn = '{"rowId": 3, "id": "0003", "favouriteColour": "blue"}'
        expectedHttpCode = '504'
        messagesToFind = [LOG_POINT_1,
                          LOG_POINT_9.format('0'),
                          LOG_POINT_9.format('1'),
                          LOG_POINT_9.format('2'),
                          LOG_POINT_11,
                          LOG_POINT_3]
        
        with self.assertRaises(ApiException) as context:
            self._postDataAndCheckResult(inputData,
                                         expectedReturn,
                                         expectedHttpCode)
        self.assertTrue(context.exception.status,
                        expectedHttpCode)
        foundAll = self._areMessagesInFile(messagesToFind,
                                           self.logFile)
        self.assertTrue(foundAll,
                        'Not all expected log points where found')
        
    def testDataCleanerPost_BadRequest(self):
        '''
        Test the a POST call to the /cleanse endpoint functions as expected.
        Ensuer that a Bad Request is handled gracefully
        '''
        # given
        inputData = 'not json'
        expectedReturn = ''
        expectedHttpCode = '400'
        messagesToFind = [LOG_POINT_1,
                          LOG_POINT_7,
                          LOG_POINT_6]

        # when 
        with self.assertRaises(ApiException) as context:
            self._postDataAndCheckResult(inputData,
                                         expectedReturn,
                                         expectedHttpCode)
        # then
        self.assertTrue(context.exception.status,
                        expectedHttpCode)
        foundAll = self._areMessagesInFile(messagesToFind,
                                           self.logFile)
        self.assertTrue(foundAll,
                        'Not all expected log points where found')
        
        
        
    def _postDataAndCheckResult(self,
                                inputData,
                                expectedReturn,
                                expectedHttpCode=200,
                                messagesToFind=[]):
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
        foundAll = self._areMessagesInFile(messagesToFind,
                                           self.logFile)
        self.assertTrue(foundAll,
                        'Not all expected log points where found')
        
    def _areMessagesInFile(self,
                         messages,
                         file):
        '''
        Determine if the given messages are all present in the given file
        '''
        notFound = len(messages)
        for line in file.readlines():
            for message in messages:
                if message in line:
                    notFound -= 1
        if notFound == 0:
            return True
        return False


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDataCleanerGet']
    unittest.main()
    