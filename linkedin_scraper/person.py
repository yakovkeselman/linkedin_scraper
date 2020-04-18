from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .functions import time_divide
from .objects import Experience, Education, Scraper

class Person(Scraper):
    __TOP_CARD = "pv-top-card"
    name = None
    experiences = []
    educations = []
    location = None
    also_viewed_urls = []
    linkedin_url = None

    def __init__(self, linkedin_url=None, name=None, experiences=[], educations=[], driver=None, get=True, scrape=True):
        self.linkedin_url = linkedin_url
        self.name = name
        self.experiences = experiences or []
        self.educations = educations or []

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
        driver.get(linkedin_url)

    def to_dict(self):
        return {
            'name': self.name,
            'url': self.linkedin_url,
            'experience': [exp.to_dict() for exp in self.experiences],
            'education': [ed.to_dict() for ed in self.educations],
        }

<<<<<<< HEAD
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
=======

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_location(self, location):
        self.location=location
    
    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete = close_on_complete)
        else:
            self.scrape_not_logged_in(close_on_complete = close_on_complete)

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        root = driver.find_element_by_class_name(self.__TOP_CARD)
        self.name = root.find_elements_by_xpath("//section/div/div/div/*/li")[0].text.strip()

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

        _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "experience-section")))

        # get experience
        exp = driver.find_element_by_id("experience-section")
        for position in exp.find_elements_by_class_name("pv-position-entity"):
            position_title = position.find_element_by_tag_name("h3").text.strip()
            company = position.find_element_by_class_name("pv-entity__secondary-title").text.strip()

            try:
                times = position.find_element_by_class_name("pv-entity__date-range").text.strip()
                times = "\n".join(times.split("\n")[1:])
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date, duration = ("Unknown", "Unknown", "Unknown")
            try:
                location = position.find_element_by_class_name("pv-entity__location").text.strip()
            except:
                location = None
            experience = Experience( position_title = position_title , from_date = from_date , to_date = to_date, duration = duration, location = location)
            experience.institution_name = company
            self.add_experience(experience)
        
        # get location
        location = driver.find_element_by_class_name(f'{self.__TOP_CARD}--list-bullet')
        location = location.find_element_by_tag_name('li').text
        self.add_location(location)

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "education-section")))

        # get education
        edu = driver.find_element_by_id("education-section")
        for school in edu.find_elements_by_class_name("pv-education-entity"):
            university = school.find_element_by_class_name("pv-entity__school-name").text.strip()
            degree = "Unknown Degree"
            try:
                degree = school.find_element_by_class_name("pv-entity__degree-name").text.strip()
                times = school.find_element_by_class_name("pv-entity__dates").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date = ("Unknown", "Unknown")
            education = Education(from_date = from_date, to_date = to_date, degree=degree)
            education.institution_name = university
            self.add_education(education)

        if close_on_complete:
            driver.close()


    def scrape_not_logged_in(self, close_on_complete=True, retry_limit=10):
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1


        # get name
        self.name = driver.find_element_by_id("name").text.strip()

        # get experience
        exp = driver.find_element_by_id("experience")
        for position in exp.find_elements_by_class_name("position"):
            position_title = position.find_element_by_class_name("item-title").text.strip()
            company = position.find_element_by_class_name("item-subtitle").text.strip()

            try:
                times = position.find_element_by_class_name("date-range").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date, duration = (None, None, None)

            try:
                location = position.find_element_by_class_name("location").text.strip()
            except:
                location = None
            experience = Experience( position_title = position_title , from_date = from_date , to_date = to_date, duration = duration, location = location)
            experience.institution_name = company
            self.add_experience(experience)

        # get education
        edu = driver.find_element_by_id("education")
        for school in edu.find_elements_by_class_name("school"):
            university = school.find_element_by_class_name("item-title").text.strip()
            degree = school.find_element_by_class_name("original").text.strip()
            try:
                times = school.find_element_by_class_name("date-range").text.strip()
                from_date, to_date, duration = time_divide(times)
            except:
                from_date, to_date = (None, None)
            education = Education(from_date = from_date, to_date = to_date, degree=degree)
            education.institution_name = university
            self.add_education(education)
>>>>>>> upstream/master

        if close_on_complete:
            driver.close()

    def __repr__(self):
        return "{name}\n\nExperience\n{exp}\n\nEducation\n{edu}".format(name=self.name, exp=self.experiences, edu=self.educations)
