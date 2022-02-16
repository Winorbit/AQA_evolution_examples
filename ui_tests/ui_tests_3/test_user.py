import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import pytest


def test_signup(driver, fake_user_payload, root_url_ui, root_url_api):
	signup_url = f"{root_url_ui}/signup"
	api_users_url = f"{root_url_api}/users"

	driver.get(signup_url)

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormLogin"]')
	login_field.send_keys(fake_user_payload.get("username"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(fake_user_payload.get("email"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(fake_user_payload.get("password"))

	signup_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button")
	signup_button.click()

	res = requests.get(api_users_url)
	users = res.json()
	new_user = [u for u in users if u.get("email") == fake_user_payload.get("email")][0] 
	del new_user["id"]

	assert new_user == fake_user_payload


def test_login(driver, user, root_url_ui):
	login_url = f"{root_url_ui}/login"
	cabinet_url = f"{root_url_ui}/cabinet"
	driver.get(login_url)

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(user.get("email"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(user.get("password"))

	signup_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button")
	signup_button.click()

	WebDriverWait(driver, 10).until(EC.url_to_be(cabinet_url))

	assert driver.current_url == cabinet_url
