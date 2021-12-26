import requests
import json
import random
from settings import headers, create_user_payload, create_user_invalid_payload, root_url
import unittest


get_user_expected_status = 200

create_user_expected_status = 201
update_user_expected_status = 201

create_user_fail_status = 400
update_user_fail_status = 400


class TestUsers(unittest.TestCase):
	users_url = f"{root_url}/users"


	def test_create_user_check_by_status(self):
		res = requests.post(self.users_url, data=json.dumps(create_user_payload), headers=headers)
		self.assertEqual(res.status_code, create_user_expected_status)


	def test_create_user_check_by_body(self):
		res = requests.post(self.users_url, data=json.dumps(create_user_payload), headers=headers)
		body = res.json()
		del body["id"]
		self.assertEqual(body, create_user_payload)


	def test_create_user_invalid_data(self):
		res = requests.post(self.users_url, data=json.dumps(create_user_invalid_payload), headers=headers)
		status = res.status_code
		self.assertEqual(res.status_code, create_user_fail_status)


	def test_get_users_check_by_status(self):
		res = requests.get(self.users_url)
		self.assertEqual(res.status_code, get_user_expected_status)


	def test_get_users_check_by_body(self):
		res = requests.get(self.users_url)
		body = res.json()
		self.assertTrue(type(body) is list)
			

	def test_with_errors_in_code(self):
		res = requests.get(self.users_url)
		body = res.json()
		# нет self.
		assertTrue(type(body) is list)


	@unittest.skip("This test skipped")
	def test_with_errors_in_code_skipped(self):
		res = requests.get(self.users_url)
		body = res.json()
		self.assertTrue(type(body) is list)

 	#@unittest.skipIf(env == "dev", "skip for DEV-env")

	def test_update_user_check_by_status():
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
				
		user_id = user.get("id")
		user_url = f"{users_url}/{user_id}"
		update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)
		self.assertEqual(update_user_res.status_code, update_user_expected_status)


	def test_update_user_check_by_body(self):
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
				
		user_id = user.get("id")
		user_url = f"{users_url}/{user_id}"
		update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)

		res = requests.get(user_url)
		body = res.json()
		self.assertEqual(body, user)


	def test_update_user_invalid_data(self):
		users_url = f"{root_url}/users"
		users = requests.get(users_url).json()
		if users:
			user = random.choice(users)
		else:
			logger.error(f"Users is empty: {users}")
			return False
			#AssertException

		user["email"] = "invalid_email"
				
		user_id = user.get("id")
		user_url = f"{users_url}/{user_id}"
		update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)
		self.assertEqual(update_user_res.status_code, update_user_fail_status)


	def raise_exception(self):
		raise Exception


	def test_catch_exception(self):
		self.assertRaises(Exception, self.raise_exception)


	# skip is resources is anavailable
	def test_catch_exception(self):
		res = requests.get(root_url)
		if res.status_code != 200:
			self.skipTest("external resource not available")
	
	
	@unittest.expectedFailure
	def test_endpoint_not_exist(self):
		res = requests.get(root_url)
		self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
	unittest.main()


