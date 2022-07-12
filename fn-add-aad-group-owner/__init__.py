import json
import requests
import logging
import os
import azure.functions as func
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution function')   

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse('Invalid request body', status_code = 400)
    else:
        groupId = req_body.get('groupId')
        ownerId = req_body.get('ownerId')
   
    if (groupId and ownerId):
        try: 
            url = f"https://graph.microsoft.com/v1.0/groups/{groupId}/owners/$ref"
            token = DefaultAzureCredential().get_token('https://graph.microsoft.com/.default').token
            headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
            body = {
                "@odata.id": f"https://graph.microsoft.com/v1.0/users/{ownerId}"                
            }
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
            return func.HttpResponse("Ok", status_code = 200)
        except Exception as e:
            logging.exception(e)
            return func.HttpResponse(str(e), status_code=500)
    else:
        return func.HttpResponse('Missing one or more required parameters', status_code = 400)        
