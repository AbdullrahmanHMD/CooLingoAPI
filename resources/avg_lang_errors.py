from urllib import response
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from dynamodb_utils import *
import json
from utils import *
from api import db_mgr

# --- User average language errors arguments ---------------------------------------------------------------------------------------
    
avg_lang_errors_args = reqparse.RequestParser()
avg_lang_errors_args.add_argument("email", type=str, help="The email of the user.", required=True)
avg_lang_errors_args.add_argument("session_errors", type=int, help="The last session time spent on the app by the user.", required=True)

# ------------------------------------------------------------------------------------------------------------------

class AverageLanguageErrors(Resource):
    def post(self):
        args = avg_lang_errors_args.parse_args()
        email = args['email']
        session_errors = args['session_errors']
        
        response, status = db_mgr.add_avg_lang_error(email, session_errors)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
        
    def get(self):
        email = request.args.get('email')
        
        response, status = db_mgr.get_avg_lang_error(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response