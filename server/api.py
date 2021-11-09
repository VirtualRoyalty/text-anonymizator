import time
from flask import jsonify
from flask_restful import Api, Resource
from flask_apispec.extension import FlaskApiSpec

import config
import handlers

api = Api(prefix=config.API_PREFIX)

api.add_resource(handlers.TestResource, '/test/<test_str>')
api.add_resource(handlers.TextAnonymizatorResource, '/anonymize')
api.add_resource(handlers.HTMLAnonymizatorResource, '/anonymize-html')


def create_docs(docs):
    docs.register(handlers.TestResource)
    docs.register(handlers.TextAnonymizatorResource)
    docs.register(handlers.HTMLAnonymizatorResource)
    return
