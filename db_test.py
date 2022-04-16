from dynamodb_utils import *

manager = DbManager()

user_id = 3
age = 104
email = 'test@gmail.com'
first_name = 'Testie'
last_name = 'Test'
password = '321344'

# response = manager.add_user(user_id, age, email, first_name, last_name, password)

# response = manager.get_user(user_id)
# print(response)

response = manager.delete_user(3)
print(response)