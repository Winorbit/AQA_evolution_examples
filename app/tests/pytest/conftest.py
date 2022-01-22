import pytest
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

p = os.path.abspath('./../../')
sys.path.insert(1, p)

from api.views import app
from api.models import DeclarativeBase as db

@pytest.fixture
def sqlite_session():
	print("SetUp test data...")
	# Создаем фейковую базоу SQLite, которя будет жить только в оперативной памяти
	engine = create_engine('sqlite:///:memory:')
	session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	db.metadata.create_all(bind=engine)
	return session

@pytest.fixture
def fake_app_client():
	print("SetUp test data...")
	# Создаем фейковое приложение, с фейковой базой SQLite, которя будет жить только в оперативной памяти
	fake_app = app
	fake_app.testing = True
	client = fake_app.test_client()
	return client

@pytest.fixture
def headers():
	return {'Content-type': 'application/json', 
           'Accept': 'application/json'}

@pytest.fixture
def create_user_payload():
	return {"username":"new_user", 
	        "email":"test@mail.com", 
	        "password": "123"}