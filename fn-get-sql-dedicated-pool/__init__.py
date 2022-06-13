import azure.functions as func
import logging
import json
import datetime
from azure.identity import DefaultAzureCredential
from azure.mgmt.synapse import SynapseManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution')
    
    base_url = 'https://management.azure.com'
    subscription_id = req.params.get('subscriptionId')
    resource_group_name = req.params.get('resourceGroupName')
    workspace_name = req.params.get('workspaceName')
    sql_pool_name = req.params.get('sqlPoolName')

    if (not subscription_id 
        or not resource_group_name 
        or not workspace_name 
        or not sql_pool_name):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            subscription_id = req_body.get('subscriptionId')
            resource_group_name = req_body.get('resourceGroupName')
            workspace_name = req_body.get('workspaceName')
            sql_pool_name = req_body.get('sqlPoolName')
    
    
    if (subscription_id and resource_group_name and workspace_name and sql_pool_name):
        try: 
            cred = DefaultAzureCredential()
            mgmt_client = SynapseManagementClient(cred, subscription_id, base_url)        
            sql_pool = mgmt_client.sql_pools.get(resource_group_name, workspace_name, sql_pool_name)
            # sql_pool_dict = vars(sql_pool)
            response = {
                'id' : sql_pool.id, 
                'name': sql_pool.name, 
                'type': sql_pool.type, 
                'tags': sql_pool.tags,
                'location': sql_pool.location,
                'sku': vars(sql_pool.sku), 
                'collation': sql_pool.collation,
                'provisioning_state': sql_pool.provisioning_state, 
                'status': sql_pool.status,
                'creation_date': sql_pool.creation_date.strftime('%m-%d-%Y'), 
                'storage_account_type': sql_pool.storage_account_type, 
            }
            return func.HttpResponse(json.dumps(response), status_code=200)
        except Exception as e:
            logging.exception(e)
            return func.HttpResponse(str(e), status_code=500)
    else:
        return func.HttpResponse('One or more required parameters are missing', status_code=400)
