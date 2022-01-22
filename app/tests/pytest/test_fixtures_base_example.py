import json
import uuid
import random
import string

import pytest

@pytest.fixture
def elementary_fixture():
    return "Hello World"

def test_my_first_fixture(elementary_fixture):
    assert "Hello World" == elementary_fixture

# Используем фикстуры в самом простом варианте

class User:
	def __init__(self, username=None, email=None):
		self.username = username
		self.email = email
		self.id = str(uuid.uuid4())

def generate_random_string(string_lenght:int):
	new_string = ''.join(random.choice(string.ascii_letters) for _ in range(string_lenght))
	return new_string

@pytest.fixture
def create_random_user():
	username = generate_random_string(8)
	email = f"{username}@gmail.com"
	new_user = User(username=username, email=email)
	return new_user

def test_create_user(create_random_user):
	assert isinstance(create_random_user.username, str)
	assert "@" in create_random_user.email


# Переделаем немного набор фикстур, чтобы они работали в связке

@pytest.fixture
def generate_random_string():
	new_string = ''.join(random.choice(string.ascii_letters) for _ in range(8))
	return new_string

@pytest.fixture
def create_random_user(generate_random_string):
	username = generate_random_string
	email = f"{username}@gmail.com"
	new_user = User(username=username, email=email)
	return new_user

def test_create_user(create_random_user):
	assert isinstance(create_random_user.username, str)
	assert "@" in create_random_user.email
