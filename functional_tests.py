from selenium import webdriver
from django.conf import settings

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

from django.test import LiveServerTestCase
import unittest
import time
import factory

from django.contrib.auth import get_user_model
from selenium import webdriver

User = get_user_model()

class UserFactory(factory.DjangoModelFactory):
    """This class sets up a staff user that we can use for testing using factory"""

    class Meta:
        model = User

    email = 'brian@djangonews.com'
    username = 'brian1'
    password = factory.PostGenerationMethodCall('set_password', 'qwer1234')

    is_superuser = True
    is_staff = True
    is_active = True

class NewsAppTest(LiveServerTestCase):
    """Main Tests"""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.domain = 'http://127.0.0.1:8081'
        self.user = UserFactory.create()

    def tearDown(self):
        self.browser.quit()


    def test_page_title_is_correct(self):
        self.browser.get(self.domain)
        self.assertIn('Django News', self.browser.title)


    def test_staff_can_create_and_publish_article(self):
        """
        Tests the core functionality of a staff member loging in, creating an article, then publishing that article
        """

        # staff logs into admin page
        self.browser.get(self.domain+"/admin")
        self.browser.find_element_by_id('id_username').send_keys('brian1')
        self.browser.find_element_by_id('id_password').send_keys('qwer1234')
        self.browser.find_element_by_class_name('submit-row').click()

        # navigate to homepage
        self.browser.get(self.domain)
        time.sleep(2)

        # navigate to new article page and write sample article
        self.browser.find_element_by_id('new-article').click()
        html = str(self.browser.page_source.encode('utf-8'))
        self.assertIn('Write your Django News article here', html)
        self.browser.find_element_by_id('id_title').send_keys('testing with selenium')
        self.browser.find_element_by_id('id_content').send_keys('about testing with selenium')
        self.browser.find_element_by_id('id_submit').click()
        html = str(self.browser.page_source.encode('utf-8'))
        self.assertIn('publish settings', html)

        # go back to home page and check that the article is not displayed
        self.browser.get(self.domain)
        html = str(self.browser.page_source.encode('utf-8'))
        self.assertNotIn('testing with selenium', html)

        self.browser.back()

        self.browser.find_element_by_id('toggle-publish').click()
        html = str(self.browser.page_source.encode('utf-8'))
        self.assertIn('testing with selenium', html)

    def test_public_page_reloads_when_article_is_published(self):
        browser2 = webdriver.Firefox()
        browser2.get(self.domain)
        html = browser2.page_source
        self.test_staff_can_create_and_publish_article()
        time.sleep(2)
        browser2.get(self.domain)
        html_after_publish = browser2.page_source
        self.assertNotEqual(html, html_after_publish)
        browser2.quit()

if __name__ == "__main__":
    unittest.main(warnings="ignore")