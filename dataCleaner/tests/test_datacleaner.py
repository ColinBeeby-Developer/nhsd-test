'''
This file contains unit tests for the datacleaner module
'''
import unittest

from dataCleaner.datacleaner import DataCleaner

class MockLogger(object):
    '''
    Mock logger class
    '''
    def log(self,
            _,
            __):
        '''
        Mock log method
        '''
        pass
    
class MockDataCleaner(DataCleaner):
    '''
    Mock DataCleaner class
    '''
    def __init__(self):
        '''
        Bypass construction of the DataCleaner class
        '''
        self.logger = MockLogger()


class TestDataCleaner(unittest.TestCase):
    '''
    Methods to test the DataCleaner class
    '''

    def testCleanData(self):
        '''
        Test that the cleanData method performs correctly.
        When JSON is passed back from preferenceProveder with no id
        a ValueError should be raised
        '''
        mockDataCleaner = MockDataCleaner()
        with self.assertRaises(ValueError):
            mockDataCleaner.cleanData('{"rowId": 1, "favouriteColour": "red"}',
                                  {})
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()