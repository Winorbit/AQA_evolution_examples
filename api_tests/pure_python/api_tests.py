import requests
import json
import random
from settings import logger
import pytest

host = "http://localhost"
port = "5000"
root_url = f"{host}:{port}"

headers = {'Content-type': 'application/json', 
		   'Accept': 'application/json'}

class TestUsers:
	create_user_expected_status = 201
	update_user_expected_status = 201

	create_user_fail_status = 400
	update_user_fail_status = 400

	create_user_payload = {"username":"new_user", 
						   "email":"test@mail.com", 
						   "password": "123"}

	create_user_invalid_payload = {"name":"new_user", 
						   		   "mail":"test@mail.com"}

	def test_create_user(self):
		url = f"{root_url}/users"	
		try:
			res = requests.post(url, data=json.dumps(self.create_user_payload), headers=headers)
			status = res.status_code
			if status == self.create_user_expected_status:
				try:
					body = res.json()
					if body == self.create_user_payload:
						logger.info("User were created successfully")
					else:
						logger.info(f"User were not created successfully - response is {body}")
				except Exception as e:
					message = f"Exception with jsonifying content: {e}"
					logger.error(message)
					raise Exception(message)
			else:
				logger.error(f"Creation user failed - wrong response status code: {status}")
		except Exception as e:
			message = f"Request to {url} failed with exception: {e}"
			logger.error(message)
			raise Exception(message)


	def test_create_user_invalid_data(self):
		url = f"{root_url}/users"	
		try:
			res = requests.post(url, data=json.dumps(self.create_user_invalid_payload), headers=headers)
			status = res.status_code
			if status == self.create_user_fail_status:
				logger.info("Expected result for create user with invalid payload")
			else:
				logger.error(f"User with invalid data were created successfully")
		except Exception as e:
			message = f"Request to {url} failed with exception: {e}"
			logger.error(message)
			raise Exception(message)


	def test_get_users():
		expected_status = 200
		url = f"{root_url}/users"
		try:
			res = requests.get(url)
			status = res.status_code
			if status_code == expected_status:
				try:
					body = res.json()
					if type(body) is list:
						logger.info(f"Users extraction successfully - users {body}")
						return True
					else:
						logger.info(f"Wrong body in response: {body}")
						return False
				except Exception as e:
					raise Exception(f"Failed with  {res.content}")
			else:
				logger.info(f"Getting users failed with statu-code: {status}")
				return False
		except Exception as e:
			raise Exception(f"Request to {url} failed with exception: {e}")


	def test_update_user(self):
		users_url = f"{root_url}/users"
		users = requests.get(users_url).json()
		if users:
			user = random.choice(users)
		else:
			logger.error(f"Users is empty: {users}")
			return False

		current_username = user.get("username")
		updated_username =  ''.join(random.sample(current_username,len(current_username)))
		user["username"] = updated_username
		
		try:
			user_id = user.get("id")
			user_url = f"{users_url}/{user_id}"
			update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)
			if update_user_res.status_code == self.update_user_expected_status:
				res = requests.get(user_url)
				if res.json() == user:
					logger.info(f"User was successfully updated to {user}")
					return True
				else:
					logger.info(f"User {user} is not updated")
					return False
			else:
				logger.info(f"Update user failed - response with status code: {update_user_res.status_code}")
				return False
		except Exception as e:
			message = f"Request failed with exception: {e}"
			logger.error(message)
			raise Exception(message)


	def test_update_user_invalid_data(self):
		users_url = f"{root_url}/users"
		users = requests.get(users_url).json()
		if users:
			user = random.choice(users)
		else:
			logger.error(f"Users is empty: {users}")
			return False

		user["email"] = "invalid_email"
		
		try:
			user_id = user.get("id")
			user_url = f"{users_url}/{user_id}"
			update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)
			if update_user_res.status_code == self.update_user_fail_status:
				logger.info(f"User was not updated with wrong data")
				return True
			else:
				logger.error(f"User with wrong data successfully updated with status {update_user_res.status_code}")
				return False

		except Exception as e:
			message = f"Request failed with exception: {e}"
			logger.error(message)
			raise Exception(message)