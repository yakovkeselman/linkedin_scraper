"""
A test script for scraping linked-in in Python.

pytest -s my_li_scraper.py
pytest -s my_li_scraper.py::TestSearch
pytest -s my_li_scraper.py::TestSearch::test_search2
"""

from my_li_scraper import person_profile, person_search


class TestSearch:
    """Test the search functionality."""
    def test_search1(self):
        person = ('Polina', 'Keselman', 'ADP', 'Principal Software Engineer')
        result = person_search(person)
        assert 'https://www.linkedin.com/in/polina-keselman-7b62a81/' in result

    def test_search2(self):
        person = ('Prabuddha', 'Biswas', 'Agilysys', 'CTO')
        result = person_search(person)
        assert 'https://www.linkedin.com/in/prabuddha-biswas-41a357/' in result


class TestProfile:
    """Test the profile functionality."""
    def test_profile1(self):
        url = 'https://www.linkedin.com/in/polina-keselman-7b62a81/'
        profile = person_profile(url)
        assert profile['name'] == 'Polina Keselman'
        assert len(profile['experience']) > 4
        assert profile['experience'][2]['institution'] == 'LexisNexis Inc'
        assert len(profile['education']) > 1
        assert profile['education'][0]['institution'] == 'Georgia State University'
        print(profile)

    def test_profile2(self):
        url = 'https://www.linkedin.com/in/prabuddha-biswas-41a357/'
        profile = person_profile(url)
        print(profile)
