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
                'language_level', 'lng_error_num', 'avg_lng_error_num', 'num_of_logins']


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
        
        DEFAULT_WORDS_LIST = []
        DEFAULT_LANGUAGE_LEVEL = "N/A"
        DEFAULT_LANGUAGE_ERROR_NUM = DEFAULT_AVG_LNG_ERROR_NUM = 0
        DEFUALT_NUM_OF_LOGINS = 1
        
        
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
            self.COLUMNS[10] : DEFUALT_NUM_OF_LOGINS
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
    
    
    def add_words(self, email, words : list):
        
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        try:
            user = self.USERS_TABLE.get_item(Key=key)['Item']
            new_word_list = list(user['words'])
            for word in words:
                if not (word in new_word_list):
                    new_word_list.append(word)
            
            user['words'] = set(new_word_list)
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
        
    
    def authenticate(self, email : str, password : str):
        user = self.get_user(email)
        
        status = None
        response = None
        
        if password == user['password']:
            status = 'success'
            response = user
        
        else:
            status = 'fail'
            
        return response, status        
        
    
    def add_language_level(self, email : str, lang_lvl : str):
        user = self.get_user(email)
        
        status = None
        response = None
        
        user['language_level'] = lang_lvl
        
        response = self.USERS_TABLE.put_item(Item=user)
        
        return response
    
    def get_language_level(self, email : str):
        user = self.get_user(email)
        lang_lvl = user['language_level'] 
        
        return lang_lvl
        
    
    def get_key(self, email : str):
        user_id = sha1(email.encode('utf-8')).hexdigest()
        key = {self.COLUMNS[0] : user_id}
        
        return key