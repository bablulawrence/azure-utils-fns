import json
import requests
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

def listUsers(upn, token): 
    url = f"https://graph.microsoft.com/v1.0/users?$filter=startswith(userPrincipalName, '{upn}')"        
    headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()['value']
    

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution function')   

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse('Invalid request body', status_code = 400)
    else:
        upn_list = req_body.get('upnList')        

    user_list = []
    token = DefaultAzureCredential().get_token('https://graph.microsoft.com/.default').token
    if (upn_list and isinstance(upn_list, list)):
        for upn in upn_list:
            try: 
                user_list += listUsers(upn, token)
            except Exception as e:
                logging.exception(e)
                return func.HttpResponse(str(e), status_code=500)
        return func.HttpResponse(json.dumps(user_list), status_code = 200)
    else:
        return func.HttpResponse('Missing/incorrect parameters', status_code = 400)        
