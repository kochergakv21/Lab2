
from selenium import webdriver
from bs4 import BeautifulSoup
import json

driver = webdriver.Firefox()
driver.get('http://0.0.0.0:5000/input_custom_data')
element = driver.find_element_by_name('row')
element.send_keys(3)
element = driver.find_element_by_id('send')
element.click()
driver.get('http://0.0.0.0:5000/')
element = driver.find_element_by_id('calculate')
element.click()
new_driver = webdriver.Firefox()
new_driver.get('http://0.0.0.0:5000/get_res')
soup = BeautifulSoup(new_driver.page_source)
dict_from_json = json.loads(soup.find("body").text)
print dict_from_json
new_driver.close()
driver.close()




