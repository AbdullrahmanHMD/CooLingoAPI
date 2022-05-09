from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from dynamodb_utils import *
import json
from utils import *

app = Flask(__name__)
api = Api(app)

user_add_args = reqparse.RequestParser()

COLUMNS = ['user_id', 'age', 'email',
            'first_name', 'last_name', 'password']

# Adding the query arguments:
# user_add_args.add_argument("user_id", type=str, help="The ID of the user", required=True)

# --- Adding a new user arguments -----------------------------------------------------------------------------------

user_add_args.add_argument("age", type=int, help="The age of the user", required=True)
user_add_args.add_argument("first_name", type=str, help="The first name of the user", required=True)
user_add_args.add_argument("last_name", type=str, help="The last name of the user", required=True)
user_add_args.add_argument("email", type=str, help="The email of the user", required=True)
user_add_args.add_argument("password", type=str, help="The password of the user", required=True)

# --- Deleting a  user arguments ------------------------------------------------------------------------------------

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument("email", type=str, help="The email of the user", required=True)

# --- Getting a user arguments --------------------------------------------------------------------------------------

user_get_args = reqparse.RequestParser()
user_get_args.add_argument("email", type=str, help="The email of the user", required=True)


db_mgr = DbManager()

# # TODO: Modify implementation so that it works with dynamodb
# def abort_on_user_does_not_exist(user_id):
#     if user_id not in users.keys():
#         abort(404, message="User does not exits")

# # TODO: Modify implementation so that it works with dynamodb
# def abort_on_user_exists(user_id):
#     if user_id in users.keys():
#         abort(409, message="User already exists")

class User(Resource):
    
    def get(self):
        # abort_on_user_does_not_exist(user_id)
        args = user_get_args.parse_args()
        email = args['email']
        response = db_mgr.get_user(email=email)
        
        json_response = {db_mgr.COLUMNS[0]: response[db_mgr.COLUMNS[0]],
                        db_mgr.COLUMNS[1]: str(response[db_mgr.COLUMNS[1]]),
                        db_mgr.COLUMNS[2]: response[db_mgr.COLUMNS[2]],
                        db_mgr.COLUMNS[3]: response[db_mgr.COLUMNS[3]],
                        db_mgr.COLUMNS[4]: response[db_mgr.COLUMNS[4]],
                        db_mgr.COLUMNS[5]: response[db_mgr.COLUMNS[5]]
                         }
        
        return json_response

    
    def post(self):
        # abort_on_user_exists(user_id)
        
        # the args variables stores and input dict containing
        # the user's info.
        args = user_add_args.parse_args()
        
        response, status = db_mgr.add_user(age=args['age'], first_name=args['first_name'],
                                   last_name=args['last_name'], email=args['email'],
                                   password=args['password'])

        
        json_response = {"user": {
                db_mgr.COLUMNS[1]: str(response[db_mgr.COLUMNS[1]]),
                db_mgr.COLUMNS[2]: response[db_mgr.COLUMNS[2]],
                db_mgr.COLUMNS[3]: response[db_mgr.COLUMNS[3]],
                db_mgr.COLUMNS[4]: response[db_mgr.COLUMNS[4]],
                    },
                         "status": status}
        
        
        return json_response
    
    def delete(self):
        
        # abort_on_user_does_not_exist(user_id)
        args = user_delete_args.parse_args()
        email = args['email']
        
        return db_mgr.delete_user(email=email)
    
# --- Adding a word arguments ---------------------------------------------------------------------------------------

user_add_words_args = reqparse.RequestParser()
user_add_words_args.add_argument("email", type=str, help="The email of the user", required=True)
user_add_words_args.add_argument("words", type=str, help="The list of words the user want to learn", required=True, action='append')
# --- Deleting a word arguments -------------------------------------------------------------------------------------

user_delete_words_args = reqparse.RequestParser()
user_delete_words_args.add_argument("email", type=str, help="The email of the user", required=True)
user_delete_words_args.add_argument("words", type=str, help="The list of words the user wants to delete", required=True, action='append')

# --- Getting the words list arguments ------------------------------------------------------------------------------

user_get_words_args =  reqparse.RequestParser()
user_get_words_args.add_argument("email", type=str, help="The email of the user", required=True)
# ------------------------------------------------------------------------------------------------------------------

class Word(Resource):
    def post(self):
        args = user_add_words_args.parse_args()
        email = args['email']
        words = args['words']

        return db_mgr.add_words(email=email, words=words)
    
    def delete(self):
        args = user_delete_words_args.parse_args()
        email = args['email']
        words = args['words']
        
        return db_mgr.delete_words(email=email, words=words)
    
    def get(self):
        args = user_get_words_args.parse_args()
        email = args['email']
        words = db_mgr.get_words(email) 
        return json.dumps(list(words))

# --- Adding a word arguments ---------------------------------------------------------------------------------------

lang_lvl_add_args = reqparse.RequestParser()
user_add_words_args.add_argument("email", type=str, help="The email of the user", required=True)
user_add_words_args.add_argument("words", type=str, help="The list of words the user want to learn", required=True, action='append')
# --- Deleting a word arguments -------------------------------------------------------------------------------------

user_delete_words_args = reqparse.RequestParser()
user_delete_words_args.add_argument("email", type=str, help="The email of the user", required=True)
user_delete_words_args.add_argument("words", type=str, help="The list of words the user wants to delete", required=True, action='append')

# --- Getting the words list arguments ------------------------------------------------------------------------------

user_get_words_args =  reqparse.RequestParser()
user_get_words_args.add_argument("email", type=str, help="The email of the user", required=True)
# ------------------------------------------------------------------------------------------------------------------
    
class LanguageLevel(Resource):
    def post(self):
        pass

    def get(self):
        pass
    
    
api.add_resource(User, "/users")
api.add_resource(Word, "/words")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)