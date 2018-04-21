import json
from flask import make_response
import log as log


def create_error_response(errors: [str]):
    return create_json_response(
        {'errors': errors},
        400
    )


def create_json_response(payload, status_code=200, suppress_logging=False):
    if not suppress_logging:
        log.response(status_code, payload)
    data = json.dumps(payload)
    response = make_response(data, status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


def parse_request_data(rq):
    try:
        data = rq.get_data()
        if data == b'':
            return {}
        return json.loads(data)
    except json.JSONDecodeError as e:
        log.log(e.msg)
        return {}
