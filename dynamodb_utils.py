from unittest.util import strclass
import boto3
import pandas as pd
import logger
from botocore.exceptions import ClientError
from hashlib import sha1, shake_128

class DbManager():

    def __init__(self):
    
        data = pd.read_csv('db_manager.csv')

        KEY_ID = data.loc[0,'Access key ID']
        SECRET_KEY = data.loc[0,'Secret access key']

        dynamodb_client = boto3.resource('dynamodb',
                                    region_name='eu-central-1',
                                    aws_access_key_id=KEY_ID,
                                    aws_secret_access_key=SECRET_KEY)

        # Creating the dynamodb client object.
        self.USERS_TABLE_NAME = 'Users'
        self.USERS_TABLE = dynamodb_client.Table(self.USERS_TABLE_NAME)

        # Defining the available columns in the database.
        self.COLUMNS = ['user_id', 'age', 'email',
                'first_name', 'last_name', 'password', 'words',
                'language_level', 'lng_error_num', 'avg_lng_error_num',
                'total_time_spent', 'avg_time_spent', 'num_of_logins']


    def add_user_dict(self, new_user):
        response = self.USERS_TABLE.put_item(Item=new_user)
 
        return response

    def add_user(self, age : int,
                email : str, first_name : str,
                last_name : str, password : str):
        """_summary_
            Given a user's information, adds a user to the Users database.
        Args:
            user_id (str): the ID of the user (This should be unique for each user)
            age (int): the age of the user.
            email (str): the email of the user.
            first_name (str): the first name of the user.
            last_name (str): the last name of the user.
            password (str): the password of the user.
            
        Returns:
            response: the response from the database.
        """
        user_id = sha1(email.encode('utf-8')).hexdigest()
        
        status = 'None'
        
        # DEFAULT_WORDS_LIST = []
        DEFAULT_WORDS_LIST = {}
        DEFAULT_LANGUAGE_LEVEL = "N/A"
        DEFAULT_LANGUAGE_ERROR_NUM = DEFAULT_AVG_LNG_ERROR_NUM = 0
        DEFUALT_NUM_OF_LOGINS = 1
        DEFUALT_AVG_TIME_SPENT = DEFUALT_TOTAL_TIME_SPENT = 0
        
        new_user = {
            self.COLUMNS[0] : user_id,
            self.COLUMNS[1] : age,
            self.COLUMNS[2] : email,
            self.COLUMNS[3] : first_name,
            self.COLUMNS[4] : last_name,
            self.COLUMNS[5] : password,
            self.COLUMNS[6] : DEFAULT_WORDS_LIST,
            self.COLUMNS[7] : DEFAULT_LANGUAGE_LEVEL,
            self.COLUMNS[8] : DEFAULT_LANGUAGE_ERROR_NUM,
            self.COLUMNS[9] : DEFAULT_AVG_LNG_ERROR_NUM,
            self.COLUMNS[10] : DEFUALT_TOTAL_TIME_SPENT,
            self.COLUMNS[11] : DEFUALT_AVG_TIME_SPENT,
            self.COLUMNS[12] : DEFUALT_NUM_OF_LOGINS
            }
        
        try:
            response_ = self.USERS_TABLE.put_item(Item=new_user)
            response_ = {
                self.COLUMNS[1] : age,
                self.COLUMNS[2] : email,
                self.COLUMNS[3] : first_name,
                self.COLUMNS[4] : last_name,
                self.COLUMNS[5] : password}
            status = 'success'
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            print('Could not add user with ID: %s from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)
            response_ = None
            status = 'fail'
            raise        
        return response_, status
    
    def get_user(self, email : str):
        
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        status = None
        try:
            response = self.USERS_TABLE.get_item(Key=key)['Item']
            status = 'success'
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not get user with ID: %s from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)

            response = None
            status = 'fail'
            raise        
        return response, status
    
    def delete_user(self, email : str):
        
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        try:
            response = self.USERS_TABLE.delete_item(Key=key)['ResponseMetadata']['HTTPStatusCode']
        
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not delete with ID: %s from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)
            response = None
            raise        
        
        return response
    
    # --- Word List --------------------------------------------------------------------------
    
    def add_words(self, email, words : list):
        
        user, status = self.get_user(email=email)
        
        try:
            new_word_list = user['words']

            for word in words:
                new_word_list[word] = {"level" : 1}    
                
            user['words'] = new_word_list
            response = self.USERS_TABLE.put_item(Item=user)
            
            
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            
            status = 'fail'
            raise        
        
        return user['words'], status
        
        
    def delete_words(self, email, words : list):
        
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        try:
            user = self.USERS_TABLE.get_item(Key=key)['Item']
            new_word_list = user['words']
            
            if len(user['words']) <= len(words):
                new_word_list = []    
                
            else:
                for word in words:
                    new_word_list.remove(word)
            
            user['words'] = new_word_list
            response = self.USERS_TABLE.put_item(Item=user)
            
            
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not get user with ID: %s from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)

            response = error_code
            raise        
        
        return user['words'], response
        
    def get_words(self, email):
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        user = self.USERS_TABLE.get_item(Key=key)['Item']
        words_list = user['words']
        
        return words_list
        
    def update_word(self, email, word):
        user, status = self.get_user(email=email)
        
        try:
            word_dict = user['words']
            if word in word_dict.keys():
                old_value = int(word_dict[word]["level"])
                word_dict[word] = {"level" : str(old_value + 1)}
            
            else:
                status = 'fail'
        except:
            status = 'fail'
            
        return word_dict, status
    
    # --- Login Authentication ----------------------------------------------------
    
    def authenticate(self, email : str, password : str):
        user, status = self.get_user(email)
        
        response = None
        
        if password == user['password']:
            status = 'success'
            response = user
        
        else:
            status = 'fail'
            
        return response, status        
        
    # --- Language Level ---------------------------------------------------------
    
    def add_language_level(self, email : str, lang_lvl : str):
        user, status = self.get_user(email)
        
        response = None
        
        user['language_level'] = lang_lvl
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
    
    def get_language_level(self, email : str):
        user, status = self.get_user(email)
        lang_lvl = user['language_level'] 
        
        return lang_lvl, status
    
    # --- Average time spent ----------------------------------------------------
    
    def add_avg_time(self, email : str, session_time : int):
        user, status = self.get_user(email)

        login_num = user['num_of_logins']
        total_time_spent = user['total_time_spent']
        
        user['avg_time_spent'] = (total_time_spent + session_time) // login_num
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
    
    
    def get_avg_time(self, email : str):
        user, status = self.get_user(email)

        avg_time_spent = user['avg_time_spent']
        
        return avg_time_spent, status
    
    # --- Total time spent ----------------------------------------------------
    
    def add_total_time(self, email : str, session_time : float):
        user, status = self.get_user(email)

        total_time = user['total_time_spent']
        
        user['total_time_spent'] = total_time + session_time
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
    
    
    def get_total_time(self, email : str):
        user, status = self.get_user(email)

        total_time_spent = user['total_time_spent']
        
        return total_time_spent, status
    
    # --- Average Language Errors ----------------------------------------------------
    
    def add_avg_lang_error(self, email : str, lang_errors : int):
        user, status = self.get_user(email)

        login_num = user['num_of_logins']
        avg_lng_error_num = user['avg_lng_error_num']
        
        user['avg_lng_error_num'] = (avg_lng_error_num + lang_errors) / login_num
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
    
    
    def get_avg_lang_error(self, email : str):
        user, status = self.get_user(email)

        avg_lng_error_num = user['avg_lng_error_num']
        
        return avg_lng_error_num, status
    
    # --- Total Language Errors ----------------------------------------------------
    
    def add_lang_errors(self, email : str, lang_errors : int):
        user, status = self.get_user(email)

        total_lang_errors = user['lng_error_num']
        user['lng_error_num'] = lang_errors + total_lang_errors
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
    
    
    def get_lang_errors(self, email : str):
        user, status = self.get_user(email)

        lng_error_num = user['lng_error_num']
        
        return lng_error_num, status
    
    # --- Number of logins ------------------------------------------------------
    
    def add_login_num(self, email : str):
        user, status = self.get_user(email)
        
        login_num = user['num_of_logins'] + 1
        user['num_of_logins'] = login_num
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response, status
        
    def get_login_num(self, email : str):
        user, status = self.get_user(email)
        
        login_num = user['num_of_logins']
        
        return login_num, status
    
    # ---------------------------------------------------------------------------
    
    def get_key(self, email : str):
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        return key
    