import requests

BASE = "http://127.0.0.1:5000/"

id = 1

fname = 'Walid'
lname = 'Baroudi'
email = 'wbaroudi18@ku.edu.tr'
password = 'ku0066288'


# response = requests.get(f'{BASE}user/{id}')
# print(response.json())


response = requests.post(f'{BASE}user/{id}', {'first_name' : fname,
                                             'last_name' : lname,
                                             'email' : email,
                                             'password' : password})
print(response.json())
