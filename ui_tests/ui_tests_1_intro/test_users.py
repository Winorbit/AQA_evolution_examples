import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import pytest

root_url_ui = "http://localhost:5001"
root_url_api = "http://localhost:5000"

fake_user = {"username":"testuser", "email":"test@gmail.com", "password":"testpass123A"}
headers = {'Content-type': 'application/json', 
           'Accept': 'application/json'}

def test_signup():
	session = webdriver.Chrome('/usr/bin/chromedriver')
	signup_url = f"{root_url_ui}/signup"
	api_users_url = f"{root_url_api}/users"

	session.get(signup_url)

	login_field = session.find_element(By.XPATH, '//*[@id="exampleDropdownFormLogin"]')
	login_field.send_keys(fake_user.get("username"))

	login_field = session.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(fake_user.get("email"))

	login_field = session.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(fake_user.get("password"))

	signup_button = session.find_element(By.XPATH, "/html/body/div/div/form/button").click()

	res = requests.get(api_users_url)
	users = res.json()
	new_user = [user for user in users if user.get("email") == "test@gmail.com"][0] 
	del new_user["id"]
	
	assert new_user == fake_user

	session.close()

def test_login():
	login_url = f"{root_url_ui}/login"
	cabinet_url = f"{root_url_ui}/cabinet"

	session = webdriver.Chrome('/usr/bin/chromedriver')
	session.get(login_url)

	api_users_url = f"{root_url_api}/users"
	res = requests.get(api_users_url)
	users = res.json()
	if users:
		user = random.choice(users)
	else:
		res = requests.post(users_url, json=fake_user, headers=headers)
		user = fake_user

	login_field = session.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(user.get("email"))

	login_field = session.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(user.get("password"))

	signup_button = session.find_element(By.XPATH, "/html/body/div/div/form/button").click()

	WebDriverWait(session, 10).until(EC.url_to_be(cabinet_url))

	assert session.current_url == cabinet_url

	session.close()
