from audioop import avg
import logging
from collections import namedtuple
from urllib import response
from statistics import mean
import azure.functions as func
import azure.durable_functions as df

Params = namedtuple('Params', ['server', 'database', 'output', 'query'])


def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("Starting execution of orchastrator function")

    #Get input parameters
    input = context.get_input()
    if 'load' in input:
        load = input['load']
    else: 
        load = 1

    if 'output' in input:
        output = input['output']
    else: 
        output = 'stats'

    params = Params(input['server'], input['database'], input['output'], input['query'])        
    query_result_tasks = [ context.call_activity('fn-drbl-query-sql-db-activity', params) for x in range(load)]
    query_results = yield context.task_all(query_result_tasks)
    if (output == 'stats'):
        avg_exec_time = mean(query_results)
        return { "avgExecTime": avg_exec_time, "queryResults": query_results, }
    else: 
        return query_results

main = df.Orchestrator.create(orchestrator_function)