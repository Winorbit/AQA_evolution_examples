import os
import sys
import pytest
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

p = os.path.abspath('.')
sys.path.insert(1, p)

from api.views import app
from api.models import User, DeclarativeBase as db
from .settings import headers, create_user_payload, create_user_invalid_payload

basedir = os.path.abspath(os.getcwd())

# class TestAPI(unittest.TestCase):
# 	def setUp(self):
# 		print("SetUp test data...")
# 		# Создаем фейковое приложение, с фейковой базой SQLite, которя будет жить только в оперативной памяти
# 		self.app = app
# 		self.app.testing = True
# 		self.client = self.app.test_client()
# 		self.engine = create_engine('sqlite:///:memory:')
# 		self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
# 		db.metadata.create_all(bind=self.engine)


# 	def tearDown(self):
# 		print("Clean up test data...")
# 		# self.session.remove()
# 		db.metadata.drop_all(bind=self.engine)



def test_validate_valid_email(self):
	valid_email = "myemail@gmail.com"
	assert True == check_email(valid_email)



#простейший прмер того, как работает фикстура - ок и не ок