import logging
from collections import namedtuple
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


Params = namedtuple('Params', ['subscriptionId', 
                              'resourceGroupName', 
                              'location'
                              'usage', 
                              'msxEngagementId'])

def main(params: Params) -> str:
    logging.info('Starting execution of the activity function')   
    subscription_id, resource_group_name, location, usage, msxEngagementId = params    
    if (subscription_id and resource_group_name and location and usage and msxEngagementId):
        try: 
            cred = DefaultAzureCredential()
            logging.error("subscription_id :" + subscription_id)
            resource_client = ResourceManagementClient(cred, subscription_id)
            rg_result = resource_client.resource_groups.create_or_update(
                    resource_group_name,
                    {
                        "location": location,
                        "tags": { "Usage":usage, "MsxEngagementId": msxEngagementId }
                    }
                )
            return { 
                "id": rg_result.id, 
                "name": rg_result.name,
                "location": rg_result.location,
                "tags": rg_result.tags 
            }
        except Exception as e:
            logging.exception(e)
            return str(e)
    else:
        return 'One or more required parameters are missing'
