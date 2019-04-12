import time
import requests
from selenium import webdriver

driver = webdriver.Firefox(executable_path='/home/faith/geckodriver')
driver.get('http://127.0.0.1:5000')
driver.maximize_window()

broken_links = []
links = driver.find_elements_by_css_selector("a")
for link in links:
    r = requests.head(link.get_attribute('href'))
    print(link.get_attribute('href'), r.status_code)
    if r.status_code <= 400:
        pass
    else:
        broken_links.append(link.get_attribute('href'))
        print(link.get_attribute('href') + " is a broken link")

driver.close()

if len(broken_links) == 0:
    print ("No broken links!")
else:
    print("This is a list of broken links: " + broken_links)
