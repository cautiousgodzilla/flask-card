from werkzeug.exceptions import HTTPException
from flask import make_response
import json



class putd_error(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":str(error_code), "error_message":str(error_message)}
        self.response= make_response(json.dumps(message), status_code)

class puts_error(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":str(error_code), "error_message":str(error_message)}
        self.response= make_response(json.dumps(message), status_code)


        