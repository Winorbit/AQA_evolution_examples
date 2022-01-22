import os
import sys
import json

import pytest

p = os.path.abspath('./../../')
sys.path.insert(1, p)

from api.models import User

def test_example_work_with_test_database(sqlite_session):
	res = sqlite_session.query(User).all()
	users = [user.serialize for user in res]
	# Убедимся в этом ,сравнив пустой список и список юзеров в базе
	# assert users == ""
	assert users == []

	# создаем для нее нового юзера 
	new_user = User(username = 'TestName', email = 'testuser@example.com', password = 12345)
	sqlite_session.add(new_user)
	sqlite_session.commit()
	res = sqlite_session.query(User).all()
	users = [user.serialize for user in res]
	# Теперь assert падает - ведь мы добавили нового юзера в тестовую базу
	# assert users == []

def test_create_user(fake_app_client, create_user_payload, headers):
	# Создаем юзера используя client фейкового приложения
	create_user_res = fake_app_client.post('/users', data=json.dumps(create_user_payload), headers=headers)
	status_code = create_user_res.status_code
	new_user_id = create_user_res.json.get("id")
	# Убеждаемся в том, что код ответа соответствует ожидаемому
	assert status_code == 201

	# Теперь убедимся в том, что юзер корректно создаан и теперь его можно извлечь через эндпоинт
	user_res = fake_app_client.get(f"/users/{new_user_id}")
	user_res_body = user_res.json
	del user_res_body["id"]
	assert create_user_payload == user_res_body
