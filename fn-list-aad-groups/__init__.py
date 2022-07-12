import json
import requests
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

def listGroups(groupName, token): 
    url = f"https://graph.microsoft.com/v1.0/groups?$filter=startswith(displayName, '{groupName}')"        
    headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['value']
    

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution function')   

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse('Invalid request body', status_code = 400)
    else:
        group_name_list = req_body.get('groupNameList')        

    group_list = []
    token = DefaultAzureCredential().get_token('https://graph.microsoft.com/.default').token
    if (group_name_list and isinstance(group_name_list, list)):
        for groupName in group_name_list:
            try: 
                group_list += listGroups(groupName, token)
            except Exception as e:
                logging.exception(e)
                return func.HttpResponse(str(e), status_code=500)
        return func.HttpResponse(json.dumps(group_list), status_code = 200)
    else:
        return func.HttpResponse('Missing/incorrect parameters', status_code = 400)        
