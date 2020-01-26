'''
This file contains classes and methods to expose the DataCleaner API
'''
from __future__ import print_function
from flask import Flask
from flask_restplus import Resource, Api, abort
import uuid

from dataCleaner.datacleaner import DataCleaner
from queryPreferenceProvider.querypreferenceprovider import QueryPreferenceProvider
from cleanerLogging.logger import Logger


app = Flask(__name__)
api = Api(app,
          title='Data Cleaner',
          description='An API to clean a persons data')

@api.route('/cleanse/<personData>')
@api.doc(params={'personData': 'The data to cleanse'})
class DataCleanerApi(Resource):
    '''
    Class exposes the cleanse endpoint
    '''
    
    def __init__(self, _):
        '''
        Constructor
        '''
        self.logger = Logger()
        queryProvider = QueryPreferenceProvider(self.logger)
        self.dataCleaner = DataCleaner(self.logger,
                                       queryProvider)
    
    def post(self, personData):
        '''
        Post data for cleansing
        '''
        internalID = uuid.uuid4()
        logDict = {'internalID': internalID}
        try:
            self.logger.log('CLEANER0001',
                            logDict)
            cleanedData = self.dataCleaner.cleanData(personData,
                                                     logDict)
        except ValueError:
            self.logger.log('CLEANER0006',
                            logDict)
            abort(400)
        except Exception:
            self.logger.log('CLEANER0003',
                            logDict)
            abort(504)
        self.logger.log('CLEANER0002',
                        logDict)
        return cleanedData

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    