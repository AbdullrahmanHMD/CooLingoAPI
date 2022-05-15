from urllib import response
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from dynamodb_utils import *
import json
from utils import *

app = Flask(__name__)
api = Api(app)


COLUMNS = ['user_id', 'age', 'email',
            'first_name', 'last_name', 'password']

# --- Adding a new user arguments -----------------------------------------------------------------------------------

user_add_args = reqparse.RequestParser()
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
        email = request.args.get('email')
        response, status = db_mgr.get_user(email=email)
        
        json_response = {"user":{db_mgr.COLUMNS[0]: response[db_mgr.COLUMNS[0]],
                        db_mgr.COLUMNS[1]: str(response[db_mgr.COLUMNS[1]]),
                        db_mgr.COLUMNS[2]: response[db_mgr.COLUMNS[2]],
                        db_mgr.COLUMNS[3]: response[db_mgr.COLUMNS[3]],
                        db_mgr.COLUMNS[4]: response[db_mgr.COLUMNS[4]],
                        db_mgr.COLUMNS[5]: response[db_mgr.COLUMNS[5]]
                         }, "status": status}
        
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
        response, _ = db_mgr.add_words(email=email, words=words)
        return {"words": list(response)}
    
    def delete(self):
        args = user_delete_words_args.parse_args()
        email = args['email']
        words = args['words']
        response, _ = db_mgr.delete_words(email=email, words=words)
        return {"words": list(response)}
    
    def get(self):
        email = request.args.get('email')
        words = db_mgr.get_words(email) 
        
        return {"words": list(words)}

# --- Adding language level arguments ---------------------------------------------------------------------------------------

lang_lvl_add_args = reqparse.RequestParser()
lang_lvl_add_args.add_argument("email", type=str, help="The email of the user", required=True)
lang_lvl_add_args.add_argument("lang_lvl", type=str, help="The language level of the user", required=True)

# --- Updating language level arguments -------------------------------------------------------------------------------------

lang_lvl_update_args = reqparse.RequestParser()
lang_lvl_update_args.add_argument("email", type=str, help="The email of the user", required=True)
lang_lvl_update_args.add_argument("lang_lvl", type=str, help="The new language level of the user", required=True)

# --- Getting language level arguments ------------------------------------------------------------------------------

lang_lvl_get_args =  reqparse.RequestParser()
lang_lvl_get_args.add_argument("email", type=str, help="The email of the user", required=True)

# ------------------------------------------------------------------------------------------------------------------

class LanguageLevel(Resource):
    def post(self):
        args = lang_lvl_add_args.parse_args()
        
        email = args['email']
        lang_lvl = args['lang_lvl']
        
        response = db_mgr.add_language_level(email=email, lang_lvl=lang_lvl)
        
        return response

    def get(self):
        email = request.args.get('email')
        
        response = db_mgr.get_language_level(email=email)
        
        return response
    
    def patch(self):
        args = lang_lvl_update_args.parse_args()
        
        email = args['email']
        lang_lvl = args['lang_lvl']
        
        response = db_mgr.add_language_level(email=email, lang_lvl=lang_lvl)
        
        return response

# --- User authentication arguments ---------------------------------------------------------------------------------------
    
login_args = reqparse.RequestParser()
login_args.add_argument("email", type=str, help="", required=True)
login_args.add_argument("password", type=str, help="", required=True)

# ------------------------------------------------------------------------------------------------------------------
    
class Authentication(Resource):
    def post(self):
        args = login_args.parse_args()
        email = args['email']
        password = args['password']
        response, status = db_mgr.authenticate(email=email, password=password)
        
        return response, status

class Questions(Resource):
    def get(self):
        from question_extractor import QUESTIONS_JSON_ARRAY
        return QUESTIONS_JSON_ARRAY



# --- User total time spent arguments ---------------------------------------------------------------------------------------
    
total_time_spent_args = reqparse.RequestParser()
total_time_spent_args.add_argument("email", type=str, help="The email of the user.", required=True)
total_time_spent_args.add_argument("session_time", type=int, help="The last session time spent on the app by the user.", required=True)

# ------------------------------------------------------------------------------------------------------------------

class TotalTimeSpent(Resource):
    
    def post(self):
        args = total_time_spent_args.parse_args()
        email = args['email']
        session_time = args['total_time']
        
        response, status = db_mgr.add_total_time(email, session_time)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
    
    def get(self):
        email = request.args.get('email')
        
        response, status = db_mgr.get_total_time(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response

# --- User average time spent arguments ---------------------------------------------------------------------------------------
    
avg_time_spent_args = reqparse.RequestParser()
avg_time_spent_args.add_argument("email", type=str, help="The email of the user.", required=True)
avg_time_spent_args.add_argument("session_time", type=int, help="The last session time spent on the app by the user.", required=True)

# ------------------------------------------------------------------------------------------------------------------

class AverageTimeSpent(Resource):
    def post(self):
        args = avg_time_spent_args.parse_args()
        email = args['email']
        session_time = args['session_time']
        
        response, status = db_mgr.add_avg_time(email, session_time)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
    
    def get(self):
        email = request.args.get('email')
        
        response, status = db_mgr.get_avg_time(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response

# --- User language errors arguments ---------------------------------------------------------------------------------------
    
total_lang_errors_args = reqparse.RequestParser()
total_lang_errors_args.add_argument("email", type=str, help="The email of the user.", required=True)
total_lang_errors_args.add_argument("session_errors", type=int, help="The last session time spent on the app by the user.", required=True)

# ------------------------------------------------------------------------------------------------------------------

class LanguageErrors(Resource):
    def post(self):
        args = total_lang_errors_args.parse_args()
        email = args['email']
        session_errors = args['session_errors']
        
        response, status = db_mgr.add_lang_errors(email, session_errors)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
    
    def get(self):
        email = request.args.get('email')
        
        response, status = db_mgr.get_lang_errors(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
    


# --- User login number arguments ---------------------------------------------------------------------------------------
    
# login_num_args = reqparse.RequestParser()
# login_num_args.add_argument("email", type=str, help="The email of the user.", required=True)

# ------------------------------------------------------------------------------------------------------------------

class LoginNumber(Resource):
    def post(self):
        email = request.args.get('email')
        response, status = db_mgr.add_login_num(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response
    
    def get(self):
        email = request.args.get('email')
        response, status = db_mgr.get_login_num(email)
        
        json_response = jsonify(response=response, status=status)
        
        return json_response

from resources.avg_lang_errors import AverageLanguageErrors

api.add_resource(Authentication, "/auth")    
api.add_resource(User, "/users")
api.add_resource(Word, "/words")
api.add_resource(LanguageLevel, "/lang_lvl")
api.add_resource(Questions, "/questions")

api.add_resource(TotalTimeSpent, "/total_time")
api.add_resource(AverageTimeSpent, "/avg_time")
api.add_resource(LanguageErrors, "/lang_errors")
api.add_resource(AverageLanguageErrors(db_mgr), "/avg_lang_errors")
api.add_resource(LoginNumber, "/login_num")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)