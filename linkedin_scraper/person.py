import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .functions import time_divide
from .objects import Experience, Education, Scraper
import os

class Person(Scraper):
    name = None
    experiences = []
    educations = []
    also_viewed_urls = []
    linkedin_url = None

    def __init__(self, linkedin_url=None, name=None, experiences=[], educations=[], driver=None, get=True, scrape=True):
        self.linkedin_url = linkedin_url
        self.name = name
        self.experiences = experiences
        self.educations = educations

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), 'drivers/chromedriver')
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape()


    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    @staticmethod
    def to_str(s1):
        s2 = ''.join([chr(c) for c in s1 if c < 128])
        s3 = s2.replace('\n', ' ')
        return ' '.join([elt for elt in s3.split(' ') if len(elt) > 0])

    def scrape(self, close_on_complete=True, timeout=3):
        driver = self.driver
        self.name = driver.find_element_by_class_name("pv-top-card-section__name").text.encode('utf-8').strip()
        self.name = self.to_str(self.name)

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        try:
            _ = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "experience-section")))

            # get experience
            exp = driver.find_element_by_id("experience-section")
            for position in exp.find_elements_by_class_name("pv-position-entity"):
                position_title = position.find_element_by_tag_name("h3").text.encode('utf-8').strip()
                position_title = self.to_str(position_title)
                try:
                    company = position.find_element_by_class_name("pv-entity__secondary-title").text.encode('utf-8').strip()
                    company = self.to_str(company)
                except NoSuchElementException:
                    company = 'Unknown'

                try:
                    times = position.find_element_by_class_name("pv-entity__date-range").text.encode('utf-8').strip()
                    times = self.to_str(times)
                    from_date, to_date = time_divide(times)
                except:
                    from_date, to_date = (None, None)
                experience = Experience(position_title=position_title, from_date=from_date, to_date=to_date)
                experience.institution_name = company
                self.add_experience(experience)
        except TimeoutException:
            pass

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        try:
            _ = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "education-section")))

            # get education
            edu = driver.find_element_by_id("education-section")
            for school in edu.find_elements_by_class_name("pv-profile-section__sortable-item"):
                try:
                    university = school.find_element_by_class_name("pv-entity__school-name").text.encode('utf-8').strip()
                    university = self.to_str(university)
                    degree = school.find_element_by_class_name("pv-entity__degree-name").text.encode('utf-8').strip()
                    degree = self.to_str(degree)
                    times = school.find_element_by_class_name("pv-entity__dates").text.encode('utf-8').strip()
                    times = self.to_str(times)
                    from_date, to_date = time_divide(times)
                    education = Education(from_date=from_date, to_date=to_date, degree=degree)
                    education.institution_name = university
                    self.add_education(education)
                except:
                    pass
        except TimeoutException:
            pass

        if close_on_complete:
            driver.close()

    def __repr__(self):
        return "{name}\n\nExperience\n{exp}\n\nEducation\n{edu}".format(name=self.name, exp=self.experiences, edu=self.educations)
