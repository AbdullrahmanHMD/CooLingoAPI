from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

user_add_args = reqparse.RequestParser()

user_add_args.add_argument("first_name", type=str, help="The first name of the user", required=True)
user_add_args.add_argument("last_name", type=str, help="The last name of the user", required=True)
user_add_args.add_argument("email", type=str, help="The email of the user", required=True)
user_add_args.add_argument("password", type=str, help="The password of the user", required=True)


users = {}

def abort_on_user_does_not_exist(user_id):
    if user_id not in users.keys():
        abort(404, message="User does not exits")

def abort_on_user_exists(user_id):
    if user_id not in users.keys():
        abort(409, message="User already exists")

class User(Resource):
    def get(self, user_id):
        abort_on_user_does_not_exist(user_id)
        return users[user_id]
    
    def post(self, user_id):
        abort_on_user_exists(user_id)
        
        # the args variables stores and input dict containing
        # the user's info.
        args = user_add_args.parse_args()
        users[user_id] = args
        return users[user_id], 201 # 201: Created.
    
    def delete(self, user_id):
        
        abort_on_user_does_not_exist(user_id)
        user = users[user_id]
        del users[user_id]
        
        return user, 204


api.add_resource(User, "/user/<int:user_id>")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)