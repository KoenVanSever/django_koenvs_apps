from django.test import TestCase
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
# Create your tests here.

OPTIONS = Options()
OPTIONS.headless = True  # ! if ran from vscode, for regular terminal comment out

# ! Functional Testing: testing the interface on a level that a user would experience (clicking buttons, checking actions, checking content)
# /i for this kind of testing you need a webdriver of preference that will open the page and try actions like a user (gecko for firefox)


# class FunctionalTestCase(TestCase):

#     def setUp(self):
#         self.browser = Firefox(options=OPTIONS)
#         self.browser.get("http://localhost:8000/")

#     def test_koenvs_presence(self):
#         self.assertIn("koenvs", self.browser.page_source)

#     def tearDown(self):
#         self.browser.quit()

# ! Unit Testing: testing the underlying code for correct operation (user would never see this level)


class UnitTestCase(TestCase):

    def test_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'index.html')
