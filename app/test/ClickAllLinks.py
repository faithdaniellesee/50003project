import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(executable_path='/home/faith/geckodriver')
driver.get('http://127.0.0.1:5000')
driver.maximize_window()

driver.find_element_by_id("username").send_keys("member")
time.sleep(1)
driver.find_element_by_id("password").send_keys("Password1")
time.sleep(1)
driver.find_element_by_id("submit").click()
time.sleep(2)

driver.find_element_by_link_text("Ticket").click()
time.sleep(3)
driver.find_element_by_link_text("Submissions").click()
time.sleep(3)
driver.find_element_by_link_text("Logout").click()
time.sleep(1)

driver.find_element_by_id("username").send_keys("admin")
time.sleep(1)
driver.find_element_by_id("password").send_keys("Password1")
time.sleep(1)
driver.find_element_by_id("submit").click()
time.sleep(1)

driver.find_element_by_link_text("Ticket").click()
time.sleep(3)
driver.find_element_by_link_text("Submissions").click()
time.sleep(3)
driver.find_element_by_link_text("Logout").click()
time.sleep(1)

driver.find_element_by_link_text("Sign Up").click()
time.sleep(1)
driver.find_element_by_id("inputEmail").send_keys("member4@example.com")
time.sleep(1)
driver.find_element_by_id("username").send_keys("member4")
time.sleep(1)
driver.find_element_by_id("password").send_keys("Password1")
time.sleep(1)
driver.find_element_by_id("password2").send_keys("Password1")
time.sleep(1)
driver.find_element_by_id("submit").click()
time.sleep(3)
