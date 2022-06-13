import logging
import json
from collections import namedtuple
import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):

    ResQueryParams = namedtuple('Params', ['subscriptionId', 'query'])
    SqlDpParams = namedtuple('Params', ['subscriptionId', 'resourceGroupName', 
                                'workspaceName', 'sqlPoolName'])

    query= 'project id, name, type, properties.status, resourceGroup | where type =~ "microsoft.synapse/workspaces/sqlpools"'
    res_query_params = ResQueryParams(subscriptionId='edf6dd9d-7c4a-4bca-a997-945f3d60cf4e', query=query)
    sqldp_params = SqlDpParams(subscriptionId ='edf6dd9d-7c4a-4bca-a997-945f3d60cf4e', 
                     resourceGroupName = 'azdemo101-rg-zrlx4',
                     workspaceName= 'azsynapsewksxqwjeq',
                     sqlPoolName= 'sqldp01')

    sqldp_list = yield context.call_activity('fn-drbl-query-resource-graph-activity', res_query_params)
    result2 = yield context.call_activity('fn-drbl-pause-sql-dp-activity', sqldp_params)
    return [sqldp_list, result2]
    # return[result1]
    # return[result2]

main = df.Orchestrator.create(orchestrator_function)