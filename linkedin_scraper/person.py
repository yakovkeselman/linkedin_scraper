from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .functions import time_divide
from .objects import Experience, Education, Scraper


class Person(Scraper):
    """Person scraper."""
    def __init__(self, linkedin_url, driver):
        self.name = ''
        self.linkedin_url = linkedin_url
        self.experiences = []
        self.educations = []
        self.driver = driver
        driver.get(linkedin_url)

    def to_dict(self):
        return {
            'name': self.name,
            'url': self.linkedin_url,
            'experience': [exp.to_dict() for exp in self.experiences],
            'education': [ed.to_dict() for ed in self.educations],
        }

    def scrape(self, close_on_complete=True, timeout=3):
        driver = self.driver
        self.name = self.class_to_text(driver, "pv-top-card-section__name")

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        try:
            _ = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "experience-section")))

            # get experience
            exp = driver.find_element_by_id("experience-section")
            for position in exp.find_elements_by_class_name("pv-position-entity"):
                title = self.tag_to_text(position, "h3")
                try:
                    company = self.class_to_text(position, "pv-entity__secondary-title")
                except NoSuchElementException:
                    company = 'Unknown'

                try:
                    descr = self.class_to_text(position, "pv-entity__description")
                except NoSuchElementException:
                    descr = 'Unknown'

                try:
                    times = self.class_to_text(position, "pv-entity__date-range")
                    from_date, to_date = time_divide(times)
                except:
                    from_date, to_date = (None, None)

                self.experiences.append(Experience(
                    institution=company, title=title,
                    from_date=from_date, to_date=to_date,
                    description=descr
                ))
        except TimeoutException:
            pass

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        try:
            _ = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "education-section")))

            # get education
            edu = driver.find_element_by_id("education-section")
            for school in edu.find_elements_by_class_name("pv-profile-section__sortable-item"):
                try:
                    university = self.class_to_text(school, "pv-entity__school-name")
                    degree = self.class_to_text(school, "pv-entity__degree-name")
                    times = self.class_to_text(school, "pv-entity__dates")
                    from_date, to_date = time_divide(times)
                    self.educations.append(Education(
                        institution=university,
                        from_date=from_date, to_date=to_date,
                        degree=degree
                    ))
                except:
                    pass
        except TimeoutException:
            pass

        if close_on_complete:
            driver.close()

    def __repr__(self):
        return "{name}\n\nExperience\n{exp}\n\nEducation\n{edu}".format(name=self.name, exp=self.experiences, edu=self.educations)
