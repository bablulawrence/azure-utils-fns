import logging
import json
import os
from collections import namedtuple
from urllib import response
import uuid 
import azure.durable_functions as df


rgParams = namedtuple('rgParams', [ 'subscriptionId',
                                'resourceGroupName', 
                                'location',
                                'usage', 
                                'msxEngagementId'])

def uniqueString():    
    return uuid.uuid4().hex[:6]

def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("Starting execution of orchastrator function")

    #Get parameters from input
    params = context.get_input()
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    
    if ('usage' in params):
        if(params['usage'] == 'poc'):
            if not 'msxEngagementId' in params:
                return 'MSX Engagement Id is mandtory for POC'
            msx_engmt_id = params['msxEngagementId']
        else:
            msx_engmt_id = 'NA'        
        usage = params['usage']
    else: 
        usage = 'demo'
        msx_engmt_id = 'NA'

    if ('resourceGroupName' in params):
        rg_name = params['resourceGroupName']
    else: 
        rg_name = f"az-{usage}-{uniqueString()}-rg"    
    
    if ('location' in params):
        location = params['location']
    else: 
        location = "centralus"    

    # logging.error( subscription_id + "|" + rg_name + "|" +  location + "|" + usage + "|" + msx_engmt_id)
    rg_params = rgParams(subscription_id, rg_name, location, usage, msx_engmt_id )
    rg_result = yield context.call_activity('fn-drbl-create-rg-activity', rg_params)
    return rg_result

main = df.Orchestrator.create(orchestrator_function)