from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from dynamodb_utils import *

app = Flask(__name__)
api = Api(app)

user_add_args = reqparse.RequestParser()

COLUMNS = ['user_id', 'age', 'email',
            'first_name', 'last_name', 'password']

# Adding the query arguments:
user_add_args.add_argument("user_id", type=int, help="The ID of the user", required=True)
user_add_args.add_argument("age", type=int, help="The age of the user", required=True)
user_add_args.add_argument("first_name", type=str, help="The first name of the user", required=True)
user_add_args.add_argument("last_name", type=str, help="The last name of the user", required=True)
user_add_args.add_argument("email", type=str, help="The email of the user", required=True)
user_add_args.add_argument("password", type=str, help="The password of the user", required=True)

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument("user_id", type=int, help="The ID of the user", required=True)

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("user_id", type=int, help="The ID of the user", required=True)
# ------------------------------------------------------------------------------------------------------

# {"user_id": "0", "age": "24", "email": "test@email.com", "first_name": "Test", "last_name": "ABC", "password": "12345"}

db_mgr = DbManager()

db_mgr.add_user(user_id="0", age="24",
                first_name="test@email.com", last_name="Test",
                email="ABC", password="12345")

users = {}
# TODO: Modify implementation so that it works with dynamodb
def abort_on_user_does_not_exist(user_id):
    if user_id not in users.keys():
        abort(404, message="User does not exits")

# TODO: Modify implementation so that it works with dynamodb
def abort_on_user_exists(user_id):
    if user_id in users.keys():
        abort(409, message="User already exists")

class User(Resource):
    def get(self, user_id):
        # abort_on_user_does_not_exist(user_id)
        args = user_get_args.parse_args()
        return db_mgr.get_user(user_id=user_id)
    
    def post(self, user_id):
        # abort_on_user_exists(user_id)
        
        # the args variables stores and input dict containing
        # the user's info.
        args = user_add_args.parse_args()
        users[user_id] = args
        
        
        db_mgr.add_user(user_id=args['user_id'], age=args['age'],
                        first_name=args['first_name'], last_name=args['last_name'],
                        email=args['email'], password=args['password'])
        
        return print(args)
    
    def delete(self, user_id):
        
        # abort_on_user_does_not_exist(user_id)
        
        args = user_delete_args.parse_args()
        return db_mgr.delete_user(user_id=user_id)


api.add_resource(User, "/user/<int:user_id>")
# api.add_resource(User, "/user/<int:user_id>")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)