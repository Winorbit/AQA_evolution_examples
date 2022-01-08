import json
import random

import requests
import pytest

from settings import root_url, headers, create_user_payload, create_user_invalid_payload

get_user_expected_status = 200
create_user_expected_status, update_user_expected_status = 201, 201
create_user_fail_status, update_user_fail_status = 400, 400

users_url = f"{root_url}/users"

def test_create_user():
	res = requests.post(users_url, data=json.dumps(create_user_payload), headers=headers)
	body = res.json()
	del body["id"]

	assert res.status_code == create_user_expected_status
	assert body == create_user_payload


def test_create_user_invalid_data():
	res = requests.post(users_url, data=json.dumps(create_user_invalid_payload), headers=headers)
	status = res.status_code
	assert res.status_code == create_user_fail_status


def test_get_users():
	res = requests.get(users_url)
	body = res.json()
	assert res.status_code == get_user_expected_status
	assert type(body) is list


def test_update_user():
	users = requests.get(users_url).json()
	if users:
		user = random.choice(users)
	else:
		pytest.xfail("Can't find random user - users list is empty")

	current_username = user.get("username")
	updated_username =  ''.join(random.sample(current_username,len(current_username)))
	user["username"] = updated_username
			
	user_id = user.get("id")
	user_url = f"{users_url}/{user_id}"
	update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)

	res = requests.get(user_url)
	body = res.json()

	assert update_user_res.status_code == update_user_expected_status
	assert body == user


@pytest.mark.mymark
def test_update_user_invalid_data():
	users_url = f"{root_url}/users"
	users = requests.get(users_url).json()
	if users:
		user = random.choice(users)
	else:
		logger.error(f"Users is empty: {users}")
		return False

	user["email"] = "invalid_email"
		
	user_id = user.get("id")
	user_url = f"{users_url}/{user_id}"
	update_user_res = requests.put(user_url, data=json.dumps(user), headers=headers)
	assert update_user_res.status_code == update_user_fail_status

@pytest.mark.skip(reason="skiping example")					
def test_skip():
	assert 4 == 4

"""
pytest
pytest -v
pytest test_users.py
pytest test_users.py -v
pytest -k us -v
pytest -v -m mymark
"""

You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/mark.html