import json

from flask import Response
from werkzeug.exceptions import HTTPException


def abort(code, **kwargs):
    description = json.dumps(kwargs)
    response = Response(status=code, mimetype='application/json',
                        response=description)
    raise HTTPException(description=description, response=response)
