'''
This file contains classes and methods to expose the DataCleaner API
'''
from __future__ import print_function
from flask import Flask
from flask_restplus import Resource, Api, abort

from dataCleaner.datacleaner import DataCleaner
from queryPreferenceProvider.querypreferenceprovider import QueryPreferenceProvider
from integrationTests.swaggerClient.rest import ApiException


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
        queryProvider = QueryPreferenceProvider()
        self.dataCleaner = DataCleaner(queryProvider)
    
    
    def post(self, personData):
        '''
        Post data for cleansing
        '''
        try:
            cleanedData = self.dataCleaner.cleanData(personData)
        except Exception:
            abort(504)
        
        return cleanedData

if __name__ == '__main__':
    app.run(port=5000)
    