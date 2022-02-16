import os

import random
import pytest
import requests
from selenium import webdriver


API_HOST = os.environ.get('API_HOST')
if not API_HOST:
    raise Exception("HOST for API is not defined")

API_PORT = os.environ.get('API_PORT')
if not API_PORT:
    raise Exception("PORT for API is not defined")


HOST = os.environ.get('HOST')
if not HOST:
    raise Exception("HOST for UI is not defined")

PORT = os.environ.get('PORT')
if not PORT:
    raise Exception("PORT for UI is not defined")


CHROMEDRIVER = os.environ.get('CHROMEDRIVER')
if not CHROMEDRIVER:
    raise Exception("CHROMEDRIVER  is not defined")


@pytest.fixture
def root_url_api():
	return f"http://{API_HOST}:{API_PORT}"

@pytest.fixture
def root_url_ui():
	return f"http://{HOST}:{PORT}"

@pytest.fixture
def driver():
	driver = webdriver.Chrome(CHROMEDRIVER)
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
		res = requests.post(users_url, json=fake_user_payload, headers=headers)
		user = res.json()
	return user
