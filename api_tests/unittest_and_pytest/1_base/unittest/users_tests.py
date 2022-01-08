import requests
import json
import random
from settings import host, port, headers, create_user_payload, create_user_invalid_payload
import unittest

root_url = f"{host}:{port}"

# https://docs.pytest.org/en/stable/reference.html?highlight=raises#pytest.raises

get_user_expected_status = 200

create_user_expected_status = 201
update_user_expected_status = 201

create_user_fail_status = 400
update_user_fail_status = 400


class TestUsers(unittest.TestCase):
		users_url = f"{root_url}/users"

		def test_upper(self):
				self.assertEqual('foo'.upper(), 'FOO')


		def test_create_user_by_status(self):
				res = requests.post(self.users_url, data=json.dumps(create_user_payload), headers=headers)
				self.assertEqual(res.status_code, create_user_expected_status)


		def test_create_user_by_body(self):
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

		@unittest.skip("demonstrating skipping")
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
				assert update_user_res.status_code == update_user_expected_status


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
				assert body == user


		def test_update_user_invalid_data(self):
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


#assertRaises и запуск эксепшенов

# python -m unittest api_tests.py
# python -m unittest api_tests.py -v
# python -m unittest api_tests.py.test_update_user_invalid_data -v

# ; assertRaises() для проверки, что метод порождает исключение

# запуск в папке - __init__.py - ?
# показать один тест, написанный с ошибкой.
# один тест фейл
# как их скипать?
# папка без __init__.py  и с ним

# asser... - их дохрена, тут в конце есть - https://pythonworld.ru/moduli/modul-unittest.html

# передача аргументов командной строки
#@unittest.skipIf(env == "dev", "skip for DEV-env")
# классы тоже могут быть скипнуты
#    @unittest.expectedFailure
#    Свои декораторы тоже можно делать


"""
-v (--verbose) - подробный вывод.
-s (--start-directory) directory_name - директория начала обнаружения тестов (текущая по умолчанию).
-p (--pattern) pattern - шаблон названия файлов с тестами (по умолчанию test*.py).
-t (--top-level-directory) directory_name - директория верхнего уровня проекта (по умолчанию равна start-directory).
"""


"""
@unittest.skip(reason) - пропустить тест. reason описывает причину пропуска.

@unittest.skipIf(condition, reason) - пропустить тест, если condition истинно.

@unittest.skipUnless(condition, reason) - пропустить тест, если condition ложно.

@unittest.expectedFailure - пометить тест как ожидаемая ошибка.

Для пропущенных тестов не запускаются setUp() и tearDown(). 
Для пропущенных классов не запускаются setUpClass() и tearDownClass(). 
Для пропущенных модулей не запускаются setUpModule() и tearDownModule().
"""

if __name__ == '__main__':
    unittest.main()
