
# class Institution(object):
#     def __init__(self, name=None, website=None, industry=None, itype=None, headquarters=None,
#                  company_size=None, founded=None):
#         self.name = name
#         self.website = website
#         self.industry = industry
#         self.type = itype
#         self.headquarters = headquarters
#         self.company_size = company_size
#         self.founded = founded


class Institution:
    def to_dict(self):
        return vars(self)


class Experience(Institution):
    def __init__(self, institution=None, title=None, from_date=None, to_date=None, description=None):
        self.institution = institution
        self.from_date = from_date
        self.to_date = to_date
        self.description = description
        self.title = title

    def __repr__(self):
        return "{title} at {institution} from {from_date} to {to_date}; details: {description}".format(**self.to_dict())


class Education(Institution):
    def __init__(self, institution=None, from_date=None, to_date=None, degree=None):
        self.institution = institution
        self.degree = degree
        self.from_date = from_date
        self.to_date = to_date

    def __repr__(self):
        return "{degree} at {institution} from {from_date} to {to_date}".format(**self.to_dict())


class Scraper(object):
    driver = None

    def is_signed_in(self):
        try:
            self.driver.find_element_by_id("profile-nav-item")
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            pass
        return False

    @staticmethod
    def to_str(elt):
        s1 = elt.text.encode('utf-8').strip()
        s2 = ''.join([chr(c) for c in s1 if c < 128])
        s3 = s2.replace('\n', ' ')
        return ' '.join([elt for elt in s3.split(' ') if len(elt) > 0])

    def class_to_text(self, parent, elt_name):
        elt = parent.find_element_by_class_name(elt_name)
        return self.to_str(elt)

    def tag_to_text(self, parent, tag_name):
        elt = parent.find_element_by_tag_name(tag_name)
        return self.to_str(elt)
