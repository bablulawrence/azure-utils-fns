from http import client
import logging
import json
import os
from collections import namedtuple
from urllib import response
from datetime import datetime
import uuid 
import azure.durable_functions as df


rgParams = namedtuple('rgParams', [ 'subscriptionId',
                                'resourceGroupName', 
                                'location',
                                'requestType', 
                                'msxEngagementId'])
# def getRequestId():    
#     # return uuid.uuid4().hex[:6]    

def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("Starting execution of orchastrator function")

    #Get parameters from input
    params = context.get_input()
    # request_id = getRequestId()
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    
    if ('requestType' in params):
        if(params['requestType'].lower() == 'poc'):
            if not 'msxEngagementId' in params:
                return 'MSX Engagement Id is mandtory for POC'
            if not 'client' in params:
                return 'Client is mandtory for POC'
            msx_engmt_id = params['msxEngagementId']
            client = params['client']
        else:
            msx_engmt_id = 'NA'
            client = 'NA'        
        request_type = params['requestType']
    else: 
        request_type = 'demo'
        msx_engmt_id = 'NA'
        client = 'NA'

    if ('resourceGroupName' in params):
        rg_name = params['resourceGroupName']
    else: 
        rg_name = f"az-{request_type}-{params['requestId']}-rg"    
    
    if ('location' in params):
        location = params['location']
    else: 
        location = "centralus"
    
    req_params = { 
                    'id': params['requestId'],
                    'requestType': request_type,
                    'msxEngagementId' : msx_engmt_id,
                    'ownerName': params['ownerName'],
                    'ownerEmail': params['ownerEmail'],
                    'consumption': params['consumption'],
                    'client': client,
                    'teamEmails': params['teamEmails'],
                    'subscriptionId': subscription_id,
                    'resourceGroupName': rg_name,
                    'location': location,
                    'requestedDateTime': params['requestedDateTime'],
                    'approvedDateTime': params['approvedDateTime'],
                    'createdDateTime': datetime.utcnow().strftime("%Y/%m/%d, %H:%M:%S")
                }
    
    aad_group_details = {        
       'groupName' : f"az-{request_type}-{params['requestId']}-group",
       'groupDesc' : f"Security group for {request_type}, request id : {params['requestId']}"        
    }

    # db_result = yield context.call_activity('fn-drbl-create-cosmosdb-item-activity', req_params)
    # add_group_result = yield context.call_activity('fn-drbl-create-aad-security-group-activity', aad_group_details)
    # rg_params = rgParams(subscription_id, rg_name, location, request_type, msx_engmt_id )
    # rg_result = yield context.call_activity('fn-drbl-create-rg-activity', rg_params)
    # return [ db_result, rg_result]
    return [ add_group_result ]

main = df.Orchestrator.create(orchestrator_function)