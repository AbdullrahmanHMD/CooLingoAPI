import json
from flask import request, Flask
from dynamodb_utils import *

app = Flask(__name__)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)

