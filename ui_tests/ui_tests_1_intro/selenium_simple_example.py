from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests


driver = webdriver.Chrome('/usr/bin/chromedriver')

driver.get("http://www.python.org")
assert "Python" in driver.title
driver.close()

driver = webdriver.Chrome()
url = "https://giuliachiola.dev/posts/oh-my-zsh-git-plugin-cheatsheet/"
driver.get(url)
my_el = driver.find_element(By.XPATH, '/html/body/div/main/article/div[2]/table[1]/tbody/tr[7]/td[1]/code')

print(my_el)
print(driver)

driver.close()

