import logging
import json
from collections import namedtuple
import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):

    Params = namedtuple('Params', ['subscriptionId', 'resourceGroupName', 
                                'workspaceName', 'sqlPoolName'])
    
    params = Params(subscriptionId ='edf6dd9d-7c4a-4bca-a997-945f3d60cf4e', 
                     resourceGroupName = 'azdemo101-rg-zrlx4',
                     workspaceName= 'azsynapsewksxqwjeq',
                     sqlPoolName= 'sqldp01')

    result1 = yield context.call_activity('fn-drbl-pause-sql-dp-activity', params)
    # result2 = yield context.call_activity('fn-drbl-pause-sql-dp-activity', "Seattle")
    # result3 = yield context.call_activity('fn-drbl-pause-sql-dp-activity', "London")
    return [result1]

main = df.Orchestrator.create(orchestrator_function)