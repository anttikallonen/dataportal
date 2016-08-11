from flask import request
from functools import wraps
from flask_login import current_app

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

def get_client_ip():
    headers_list = request.headers.getlist("X-Forwarded-For")
    client_ip = headers_list[0] if headers_list else request.remote_addr
    return client_ip
