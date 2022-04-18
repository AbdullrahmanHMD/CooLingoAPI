import json
from flask import request
from flask_lambda import FlaskLambda
from dynamodb_utils import *

app = FlaskLambda(__name__)

db_manager = DbManager()

@app.route('/users', methods=['POST'])
def put_student():
    if request.method == 'GET':
        db_manager.add_user_dict(Item=request.form.to_dict())
        
    

