import logging
import json
from collections import namedtuple
from azure.identity import DefaultAzureCredential
from pyapacheatlas.core import PurviewClient

Params = namedtuple('Params', ['accountName', 'query', 
                                'limit', 'search_filter', 
                                'starting_offset'])

def main(params: Params) -> str:
    logging.info('Starting execution of activity function')   
    accountName, query, limit, search_filter, starting_offset = params    
    if (accountName and query):
        try: 
            cred = DefaultAzureCredential()
            purview_client = PurviewClient(accountName, cred)
            result= purview_client.discovery.search_entities(query=query, 
            limit=limit, search_filter=search_filter, starting_offset=starting_offset)
            entities = []
            for entity in result:
                entities += [entity]        
            return entities
        except Exception as e:
            logging.exception(e)
            return str(e)
    else:
        return 'One or more required parameters are missing'
