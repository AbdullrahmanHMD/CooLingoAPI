import json
from flask import request
from flask_lambda import FlaskLambda
from flask_restful import Api
from dynamodb_utils import *

app = FlaskLambda(__name__)

db_manager = DbManager()

@app.route('/users', methods=['POST'])
def put_student():
    if request.method == 'POST':
        db_manager.add_user_dict(Item=request.form.to_dict())
    
    return (
        json.dumps({'message': 'User entry created'}),
        200,
        {'Content-Type': 'application/json'}
        )
    

