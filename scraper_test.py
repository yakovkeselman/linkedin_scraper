"""
A test script for scraping linked-in in Python.

Borrowed from:
https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/
https://github.com/yakovkeselman/linkedin_scraper

"""

import unittest
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


def my_send_keys(form, chars):
    """Send keys with some delay."""
    form.send_keys(chars)
    # The other versions are not working well in search window...
    # arr = chars.split(' ')
    # for elt in arr:
    #     form.send_keys(elt)
    #     sleep(0.5 * random())
    #
    # form.send_keys(chars)
    # for ch in chars:
    #     form.send_keys(ch)
    #     sleep(0.2 * random())


LI_URL = 'https://www.linkedin.com'
COOKIES = 'linkedin_cookies.pkl'


def linked_in_home() -> webdriver.Chrome:
    """Returns driver pointing to LI home page of the person."""
    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome('chromedriver')

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
        sign_in_button.click()

        cookies = driver.get_cookies()
        pickle.dump(cookies, open(COOKIES, "wb"))

    return driver


def search_for_person(driver: webdriver.Chrome, attrs: tuple) -> list:
    """Search for a single person; assumes only few results."""
    if search_for_person.counter > 0:
        # go back to an empty search window; clearing it does not work.
        driver.execute_script("window.history.go(-1)")

    ids = driver.find_elements_by_xpath('//*[@id]')
    for ii in ids:
        name = ii.get_attribute('id')
        # The search window is after the trigger element.
        if 'trigger' in name:
            continue
        new_str = name + ' ' + ' '.join(attrs) + '\n'
        try:
            my_send_keys(ii, new_str)
            break
        except:
            pass

    # TODO: need to wait for a bit; TODO: something better.
    sleep(3)
    elts = driver.find_elements_by_class_name("search-result__result-link")
    search_for_person.counter += 1
    return [elt.get_attribute("href") for elt in elts]


search_for_person.counter = 0


def profile_test():
    driver = linked_in_home()
    profile_urls = [
        'https://www.linkedin.com/in/polina-keselman-7b62a81/',
        'https://www.linkedin.com/in/jnathanhanna/',
        'https://www.linkedin.com/in/shim-onster-15b798177/',
        'https://www.linkedin.com/in/yakovkeselman/',
    ]
    shuffle(profile_urls)
    for profile_url in profile_urls:
        person = Person(profile_url, driver=driver)
        person.scrape(close_on_complete=False, timeout=10)
        print(person)
        print(3*'\n')
        sleep(2+5*random())


class TestSearch(unittest.TestCase):
    def test_search(self):
        driver = linked_in_home()

        p1 = ('Polina', 'Keselman', 'ADP', 'Principal Software Engineer')
        r1 = search_for_person(driver, p1)
        self.assertTrue('https://www.linkedin.com/in/polina-keselman-7b62a81/' in r1)

        p2 = ('Prabuddha', 'Biswas', 'Agilysys', 'CTO')
        r2 = search_for_person(driver, p2)
        self.assertTrue('https://www.linkedin.com/in/prabuddha-biswas-41a357/' in r2)


if __name__ == '__main__':
    unittest.main(warnings='ignore')

