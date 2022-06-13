import json
import logging
import datetime
import azure.functions as func

def main(eventGridEvent: func.EventGridEvent, outputEvent: func.Out[func.EventGridOutputEvent]):
    inputEvent = {
        'id': eventGridEvent.id,
        'data': eventGridEvent.get_json(),
        'topic': eventGridEvent.topic,
        'subject': eventGridEvent.subject,
        'event_type': eventGridEvent.event_type,
    }

    outputEvent.set(
        func.EventGridOutputEvent(
            id= eventGridEvent.id,
            data={"tag1": "value1", "tag2": "value2"},
            subject=eventGridEvent.subject,
            event_type=eventGridEvent.event_type,
            event_time=datetime.datetime.utcnow(),
            data_version="1.0"))

    logging.info('Python EventGrid trigger processed an event: %s', inputEvent)
    # return func.HttpResponse((result), status_code=200)
