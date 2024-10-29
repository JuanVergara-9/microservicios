import unittest
from selenium import webdriver

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        self.driver.get('http://localhost:5003')
        self.assertIn('Home', self.driver.title)

if __name__ == '__main__':
    unittest.main()