"""
A test script for scraping linked-in in Python.

Borrowed from:
https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
https://github.com/yakovkeselman/linkedin_scraper

"""

# from subprocess import call, TimeoutExpired
from os import getenv
from time import sleep
from random import random, shuffle
import pickle

from selenium import webdriver
from linkedin_scraper import Person

user_email = getenv("USER_EMAIL")
user_pwd = getenv("USER_PWD")

assert user_email, "set 'USER_EMAIL' to LI user email"
assert user_pwd, "set 'USER_PWD' to LI user password"

# try:
#     call(["chromedriver"], timeout=1)
# except TimeoutExpired:
#     pass


def my_send_keys(form, chars):
    """Send keys with some delay."""
    form.send_keys(chars)
    for ch in []: # chars:
        form.send_keys(ch)
        sleep(0.5 * random())


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('chromedriver')

LI_URL = 'https://www.linkedin.com'
COOKIES = 'linkedin_cookies.pkl'
driver.get(LI_URL)

try:
    cookies = pickle.load(open(COOKIES, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(LI_URL)

except FileNotFoundError:
    username = driver.find_element_by_class_name('login-email')
    my_send_keys(username, user_email)
    sleep(0.5+2*random())

    password = driver.find_element_by_class_name('login-password')
    my_send_keys(password, user_pwd)
    sleep(0.5+2*random())

    # locate submit button by_xpath; others don't work as well.
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

    # .click() to mimic button click
    sign_in_button.click()

    cookies = driver.get_cookies()
    pickle.dump(driver.get_cookies(), open(COOKIES, "wb"))

profile_urls = [
    'https://www.linkedin.com/in/polina-keselman-7b62a81/',
    'https://www.linkedin.com/in/jnathanhanna/',
    'https://www.linkedin.com/in/shim-onster-15b798177/',
    'https://www.linkedin.com/in/yakovkeselman/',
]
shuffle(profile_urls)
for profile_url in profile_urls:
    person = Person(profile_url, driver=driver, scrape=False)
    person.experiences = []
    person.educations = []
    person.scrape(close_on_complete=False, timeout=10)
    print(person)
    print(3*'\n')
    sleep(5+10*random())
