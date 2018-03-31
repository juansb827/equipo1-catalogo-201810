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

    def test_add_example(self):
        self.browser.get('http://localhost:8000')
        link = self.browser.find_element_by_css_selector("a[href='/catalogo/example/']")
        link.click()

        name = self.browser.find_element_by_id('name')
        name.send_keys('Test')

        url = self.browser.find_element_by_id('url')
        url.send_keys('localhost:8000')

        self.browser.find_element_by_css_selector("#tech > option:nth-child(2)").click()

        self.browser.find_element_by_css_selector("#tool > option:nth-child(2)").click()

        self.browser.find_element_by_css_selector("#formAddExample > button").click()

        self.browser.implicitly_wait(3)

        button = self.browser.find_element_by_css_selector("#formAddExample > button")

        self.assertIn('Guardar', button.text)