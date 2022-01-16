import os
import sys
import unittest
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

p = os.path.abspath('.')
sys.path.insert(1, p)

from api.views import app
from api.models import User, DeclarativeBase as db
from .settings import headers, create_user_payload, create_user_invalid_payload

basedir = os.path.abspath(os.getcwd())

class TestAPI(unittest.TestCase):
	def setUp(self):
		print("SetUp test data...")
		# Создаем фейковое приложение, с фейковой базой SQLite, которя будет жить только в оперативной памяти
		self.app = app
		self.app.testing = True
		self.client = self.app.test_client()
		self.engine = create_engine('sqlite:///:memory:')
		self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
		db.metadata.create_all(bind=self.engine)


	def tearDown(self):
		print("Clean up test data...")
		# self.session.remove()
		db.metadata.drop_all(bind=self.engine)


	def test_example_work_with_test_database(self):
		# В тестовой базе пока нет юзеров
		res = self.session.query(User).all()
		users = [user.serialize for user in res]
		# Убедимся в этом ,сравнив пустой список и список юзеров в базе
		self.assertEqual(users, [])

		# создаем для нее нового юзера 
		new_user = User(username = 'TestName', email = 'testuser@example.com', password = 12345)
		self.session.add(new_user)
		self.session.commit()
		res = self.session.query(User).all()
		users = [user.serialize for user in res]
		# Теперь assert падает - ведь мы добавили нового юзера в тестовую базу
		self.assertEqual(users,[])


	def test_create_user(self):
		# Создаем юзера используя client фейкового приложения
		create_user_res = self.client.post('/users', data=json.dumps(create_user_payload), headers=headers)
		status_code = create_user_res.status_code
		new_user_id = create_user_res.json.get("id")
		# Убеждаемся в том, что код ответа соответствует ожидаемому
		self.assertEqual(status_code, 201)

		# Теперь убедимся в том, что юзер корректно создаан и теперь его можно извлечь через эндпоинт
		user_res = self.client.get(f"/users/{new_user_id}")
		user_res_body = user_res.json
		del user_res_body["id"]
		self.assertEqual(create_user_payload, user_res_body)


if __name__ == '__main__':
    unittest.main()