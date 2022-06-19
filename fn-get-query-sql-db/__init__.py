import azure.functions as func
import logging
import json
import pyodbc
import struct
from time import time
from azure.identity import DefaultAzureCredential

def get_access_token():
        creds = DefaultAzureCredential()
        token = creds.get_token("https://database.windows.net/.default")
        tokenb = bytes(token.token, "UTF-8")
        exptoken = b''

        for i in tokenb:
            exptoken += bytes({i})
            exptoken += bytes(1)
            tokenstruct = struct.pack("=i", len(exptoken)) + exptoken    
        return tokenstruct

def execute_query(cursor, query): 
    cursor.execute(query)
    rows = []
    for row in cursor:
        rows += [[elem for elem in row]]
    return rows

    
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting execution')
  
    driver="{ODBC Driver 17 for SQL Server}"
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        server = req_body.get('server')
        database = req_body.get('database')
        output = req_body.get('output')
        query = req_body.get('query')

    if (not server or not database or not output or not query):
        func.HttpResponse("One or more required parameters are missing", status_code = 400)

    conn_string = f"DRIVER={driver};SERVER={server};DATABASE={database}"
    access_token = get_access_token()
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    try:
        with pyodbc.connect(conn_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: access_token}) as conn:
            with conn.cursor() as cursor:
                if (output == 'json'):
                    rows = execute_query(cursor, query)
                    return func.HttpResponse(json.dumps(rows), status_code=200)
                elif (output == 'stats'):
                    start_time = time()
                    rows = execute_query(cursor, query)
                    end_time = time()
                    return func.HttpResponse(json.dumps({ "executionTime" : end_time - start_time }),
                                         status_code = 200) 
                else: 
                    return func.HttpResponse('Invalid output type', status_code = 400)

    except Exception as e: 
        logging.exception(e)
        return func.HttpResponse(str(e), status_code=500)
    