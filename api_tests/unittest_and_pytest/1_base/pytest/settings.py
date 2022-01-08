host = "http://localhost"
port = "5000"
root_url = f"{host}:{port}"
headers = {'Content-type': 'application/json', 
           'Accept': 'application/json'}

create_user_payload = {"username":"new_user", 
                       "email":"test@mail.com", 
                       "password": "123"}

create_user_invalid_payload = {"name":"new_user", 
                               "mail":"test@mail.com"}