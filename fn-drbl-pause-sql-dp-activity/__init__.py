import logging
from collections import namedtuple
from azure.identity import DefaultAzureCredential
from azure.mgmt.synapse import SynapseManagementClient

Params = namedtuple('Params', ['subscriptionId', 'resourceGroupName', 
                                'workspaceName', 'sqlPoolName'])

def main(params: Params) -> str:
    logging.info('Starting execution')   
    base_url = 'https://management.azure.com'
    subscription_id, resource_group_name, workspace_name, sql_pool_name = params    
    if (subscription_id and resource_group_name and workspace_name and sql_pool_name):
        try: 
            cred = DefaultAzureCredential()
            mgmt_client = SynapseManagementClient(cred, subscription_id, base_url)        
            result = mgmt_client.sql_pools.begin_pause(resource_group_name, workspace_name, sql_pool_name)
            return f'Status of pause operation on SQL dedicated pool "{ sql_pool_name}" : "{ result.status() }".'
        except Exception as e:
            logging.exception(e)
            return str(e)
    else:
        return 'One or more required parameters are missing'
