from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import pytest

root_url_ui = "http://localhost:5001"
root_url_api = "http://localhost:5000"

driver = webdriver.Chrome('/usr/bin/chromedriver')

#fixtures!!!

def test_signup():
	signup_url = f"{root_url_ui}/signup"
	api_users_url = f"{root_url_api}/users"

	driver.get(signup_url)

	fake_user = {"username":"testuser", "email":"test@gmail.com", "password":"testpass123A"}

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormLogin"]')
	login_field.send_keys(fake_user.get("username"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(fake_user.get("email"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(fake_user.get("password"))

	signup_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button").click()

	res = requests.get(api_users_url)
	users = res.json()
	new_user = [user for user in users if user.get("email") == "test@gmail.com"][0] 
	del new_user["id"]
	assert new_user == fake_user

	driver.close()
