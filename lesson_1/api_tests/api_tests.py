import requests
import json
from settings import logger

host = "http://localhost"
port = "5000"
root_url = f"{host}:{port}"

class TestUsers:
	headers = {'Content-type': 'application/json', 
			   'Accept': 'application/json'}

	create_user_payload = {"username":"new_user", 
						   "email":"test@mail.com", 
						   "password": "123"}

	create_user_invalid_payload = {"name":"new_user", 
						   		   "mail":"test@mail.com"}

	create_user_expected_status = 201
	create_user_fail_status = 400



	def test_create_user(self):
		expected_body = {}
		url = f"{root_url}/users"	
		try:
			res = requests.post(url, data=json.dumps(self.create_user_payload), headers=self.headers)
			status = res.status_code
			if status == self.create_user_expected_status:
				try:
					body = res.json()
					if body == {}:
						logger.info("User were created successfully")
					else:
						logger.info(f"User were not created successfully - response is {body}")

				except Exception:
					message = f"Exception with jsonifying content: {res.content}"
					logger.error(message)
					raise Exception(message)
			else:
				logger.info(f"Creation user failed - wrong response status code: {status}")

		except Exception as e:
			message = f"Request to {url} failed with exception: {e}"
			logger.error(message)
			raise Exception(message)


	def test_create_user_invalid_data(self):
		url = f"{root_url}/users"	
		try:
			res = requests.post(url, data=json.dumps(self.create_user_invalid_payload), headers=self.headers)
			status = res.status_code
			print(res)
			if status is self.create_user_fail_status:
				logger.info("Expected result for create user with invalid payload")
			else:
				logger.error(f"User with invalid data were created successfully")
		except Exception as e:
			message = f"Request to {url} failed with exception: {e}"
			logger.error(message)
			raise Exception(message)





# def test_get_users():
# 	expected_status = 200
# 	url = f"{root_url}/users"
# 	try:
# 		res = requests.get(url)
# 		status = res.status_code
# 		if status_code == expected_status:
# 			try:
# 				body = res.json()
# 				if type(body) == list and len(body) > 0:
# 					logger.info("Users extraction successfully")

# 			except Exception as e:
# 				raise Exception(f"Failed with  {res.content}")

# 	except Exception as e:
# 		raise Exception(f"Request to {url} failed with exception: {e}")