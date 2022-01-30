from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

root_url_ui = "http://localhost:5001"
root_url_api = "http://localhost:5000"

driver = webdriver.Chrome('/usr/bin/chromedriver')

def test_signup():
	driver.get(f"{root_url_ui}/signup")
	try:
		login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormLogin"]')
		login_field.send_keys("testuser")

		login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
		login_field.send_keys("test@gmail.com")

		login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
		login_field.send_keys("testpass123A")

		signup_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button").click()

		res = requests.get(f"{root_url_api}/users")
		users = res.json()
		new_user = [user for user in users if user.get("email") == "test@gmail.com"]
		if new_user:
			print("PASSED: User was created successfully")
		else:
			print("FAILED: user creation failed")
	except Exception as e:
		raise Exception(f"ERROR: {e}")

	driver.close()

test_signup()
