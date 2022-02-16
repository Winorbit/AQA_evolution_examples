import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest


def test_login_and_public_post(driver, user, post, root_url_ui):
	login_url = f"{root_url_ui}/login"
	cabinet_url = f"{root_url_ui}/cabinet"
	# Находим на главной странице ссылку на страницу с авторизацией через текст ссылки
	# login_page_link = driver.find_element_by_partial_link_text('somelink') - здесь мы словим ошибку
	driver.get(root_url_ui)

	try:
		login_link = driver.find_element(By.XPATH, '//a[text()="login"]')
	except NoSuchElementException:
		raise NoSuchElementException("Can't find link on page")

	"""
	элемент может быть не видим ,например, из-за слишком узкого окна
	ElementNotInteractableException
	login_link.click()
	assert login_link.is_displayed()
	"""
	driver.set_window_size(1280, 600)  # Добавим ширины экрану, чтоб наша ссылка была видима и кликабельна
	assert login_link.is_displayed()

	login_link.click()
	WebDriverWait(driver, 10).until(EC.url_to_be(login_url))

	assert driver.current_url == login_url

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormEmail1"]')
	login_field.send_keys(user.get("email"))

	login_field = driver.find_element(By.XPATH, '//*[@id="exampleDropdownFormPassword1"]')
	login_field.send_keys(user.get("password"))

	signup_button = driver.find_element(By.XPATH, "/html/body/div/div/form/button")
	signup_button.click()

	WebDriverWait(driver, 10).until(EC.url_to_be(cabinet_url))

	assert driver.current_url == cabinet_url

	# Пример поиска по name
	post_title_field = driver.find_element(By.NAME, 'title')
	post_title_field.send_keys(post.get("title"))

	post_text_field = driver.find_element(By.NAME, 'post_text')
	post_text_field.send_keys(post.get("text"))

	public_post_button = driver.find_element(By.ID, 'public_post')
	public_post_button.click()

	# Ждем, пока не сменится ссылка на ту, что содержит в адресе posts
	WebDriverWait(driver, 10).until(EC.url_matches("posts"))

	published_post_title = driver.find_element(By.CLASS_NAME, 'card-title').text
	published_post_text = driver.find_element(By.CLASS_NAME, 'card-text').text

	assert published_post_title == post.get("title")
	assert published_post_text == post.get("text")