# encoding: utf-8

from flask_restplus import Api
from flask import Blueprint


from .auth.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
        title='SIMPLE TODO RESTPLUS SERVER',
        version='1.0',
        description='simple restplus api to ToDo manager server'
        )


api.add_namespace(user_ns, path='/user')
