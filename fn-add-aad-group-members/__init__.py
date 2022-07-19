import json
import requests
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential

def getMemberList(member_id_list):
    member_list = []
    for id in member_id_list:
        member_list.append(f"https://graph.microsoft.com/v1.0/directoryObjects/{id}")
    return member_list

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution function')   

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse('Invalid request body', status_code = 400)
    else:
        group_id = req_body.get('groupId')
        member_id_list = req_body.get('memberIdList')
   
    if (group_id and member_id_list and isinstance(member_id_list, list)):
        token = DefaultAzureCredential().get_token('https://graph.microsoft.com/.default').token
        try: 
            url = f"https://graph.microsoft.com/v1.0/groups/{group_id}"
            headers =  {"Content-Type":"application/json", "Authorization": f"Bearer {token}"}
            body = {
                "members@odata.bind": getMemberList(member_id_list)
            }            
            response = requests.patch(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
            return func.HttpResponse("Ok", status_code = 200)
        except Exception as e:
            logging.exception(e)
            return func.HttpResponse(str(e), status_code=500)
    else:
        return func.HttpResponse('Missing one or more required parameters', status_code = 400)        
