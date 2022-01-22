import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

p = os.path.abspath('./../../')
sys.path.insert(1, p)

from api.views import app
from api.models import User, DeclarativeBase as db

@pytest.fixture
def sqlite_session_fixture():
	print("SetUp test data...")
	# Создаем фейковую базоу SQLite, которя будет жить только в оперативной памяти
	engine = create_engine('sqlite:///:memory:')
	session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	db.metadata.create_all(bind=engine)
	return session
	
def test_example_work_with_test_database(sqlite_session_fixture):
	res = sqlite_session_fixture.query(User).all()
	users = [user.serialize for user in res]
	# Убедимся в этом ,сравнив пустой список и список юзеров в базе
	# assert users == ""
	assert users == []

	# создаем для нее нового юзера 
	new_user = User(username = 'TestName', email = 'testuser@example.com', password = 12345)
	sqlite_session_fixture.add(new_user)
	sqlite_session_fixture.commit()
	res = sqlite_session_fixture.query(User).all()
	users = [user.serialize for user in res]
	# Теперь assert падает - ведь мы добавили нового юзера в тестовую базу
	# assert users == []
