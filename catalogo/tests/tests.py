# encoding: utf-8
from unittest import TestCase
from selenium import webdriver


class FunctionalTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome("D:\\Descargas\\chromedriver.exe")
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:8000')
        self.assertTrue(u'Catálogo CONECTATE' == self.browser.title)
