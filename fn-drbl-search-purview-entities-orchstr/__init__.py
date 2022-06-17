import logging
import json
from collections import namedtuple
import azure.durable_functions as df

Params = namedtuple('Params', ['accountName', 'query', 
                                'limit', 'search_filter', 
                                'starting_offset'], defaults=[10, None, 0])
    
def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("Starting execution of orchastrator function")

    #Get input parameters
    input = context.get_input()
    if 'accountName' in input and 'query' in input:
        if 'limit' in input:
            limit = input['limit']
        else: 
            limit = 10
        
        if 'search_filter' in input:
            search_filter = input['search_filter']
        else: 
            search_filter = None
        
        if 'starting_offset' in input:
            starting_offset = input['starting_offset']
        else: 
            starting_offset = 0

        params = Params(input['accountName'], input['query'], limit, search_filter, starting_offset)        
        
        #Execute Purview search entity activity function
        search_results = yield context.call_activity('fn-drbl-search-purview-entities-activity', params) 
        return search_results
    else:
        return "Please provide purview account name and search query"

main = df.Orchestrator.create(orchestrator_function)