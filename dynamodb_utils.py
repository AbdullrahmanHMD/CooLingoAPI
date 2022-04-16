import boto3
import pandas as pd
import logger
from botocore.exceptions import ClientError


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
                'first_name', 'last_name', 'password']


    def add_user(self, user_id : int, age : int,
                email : str, first_name : str,
                last_name : str, password : str):
        """_summary_
            Given a user's information, adds a user to the Users database.
        Args:
            user_id (int): the ID of the user (This should be unique for each user)
            age (int): the age of the user.
            email (str): the email of the user.
            first_name (str): the first name of the user.
            last_name (str): the last name of the user.
            password (str): the password of the user.
            
        Returns:
            response: the response from the database.
        """

        new_user = {
            self.COLUMNS[0] : user_id,
            self.COLUMNS[1] : age,
            self.COLUMNS[2] : email,
            self.COLUMNS[3] : first_name,
            self.COLUMNS[4] : last_name,
            self.COLUMNS[5] : password
            }
        try:
            response = self.USERS_TABLE.put_item(Item=new_user)

        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not add user with ID: %d from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)
            response = None
            raise        
        return response
    
    def get_user(self, user_id : int):
        
        key = {self.COLUMNS[0] : user_id}
        
        try:
            response = self.USERS_TABLE.get_item(Key=key)['Item']
            
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not get user with ID: %d from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)

            response = None
            raise        
        return response
    
    def delete_user(self, user_id : int):
        key = {self.COLUMNS[0] : user_id}
        
        try:
            response = self.USERS_TABLE.delete_item(Key=key)['ResponseMetadata']['HTTPStatusCode']
        
        except ClientError as err:
            error_msg = err.response['Error']['Message']
            error_code = err.response['Error']['Code']
            logger.error('Could not delete with ID: %d from table %s. %s: %s',
                         user_id, self.USERS_TABLE_NAME,
                         error_code, error_msg)
            response = None
            raise        
        
        return response
        
    
