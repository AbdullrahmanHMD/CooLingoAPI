import boto3

ID=''
S_ID=''

dynamodb_client = boto3.resource('dynamodb', region_name='eu-central-1', aws_access_key_id=ID,
                                 aws_secret_access_key=S_ID)

users_table = 'Users'

users_table = dynamodb_client.Table(users_table)

COLUMNS = ['user_id', 'age', 'email',
           'first_name', 'last_name', 'password']


user_id = 1
age = 18
email = 'test@gmail.com'
first_name = 'Alex'
last_name = 'Bob'
password = '321'

new_user = {
    COLUMNS[0] : user_id,
    COLUMNS[1] : age,
    COLUMNS[2] : email,
    COLUMNS[3] : first_name,
    COLUMNS[4] : last_name,
    COLUMNS[5] : password
}

response = users_table.put_item(Item=new_user)

print(response)