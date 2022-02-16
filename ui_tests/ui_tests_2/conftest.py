import random
import pytest
import requests
from selenium import webdriver

@pytest.fixture
def driver():
	driver = webdriver.Chrome('/usr/bin/chromedriver')
	return driver

@pytest.fixture
def fake_user_payload():
	return {"username":"testuser", "email":"test@gmail.com", "password":"testpass123A"}

@pytest.fixture
def post():
	return {"title":"test title", "text":"test text"}

@pytest.fixture
def user(root_url_api):
	api_users_url = f"{root_url_api}/users"
	res = requests.get(api_users_url)
	users = res.json()
	if users:
		user = random.choice(users)
	else:
		res = requests.post(users_url, json=fake_user_payload)
		user = res.json()
	return user
