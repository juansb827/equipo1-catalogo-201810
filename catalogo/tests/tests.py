# encoding: utf-8
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By


class FunctionalTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
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

    #Agregar nueva prueba para login

    def test_login(self):
        self.browser.get('http://127.0.0.1:8000/')
        link =  self.browser.find_element_by_id('id_login')
        link.click()

        username = self.browser.find_element_by_id('username')
        username.send_keys('af.carrion')

        password = self.browser.find_element_by_id('password')
        password.send_keys('Natalia123')

        btnLogin = self.browser.find_element_by_id('btnLogin')
        btnLogin.click()

        a = self.browser.find_element(By.XPATH, '//a[text()="af.carrion"]')
        self.assertIn('af.carrion', a.text)

    def test_revision(self):
        self.browser.get('http://127.0.0.1:8000')
        link = self.browser.find_element_by_id('id_login')
        link.click()
        self.browser.implicitly_wait(1)

        username = self.browser.find_element_by_id('username')
        username.send_keys('af.carrion')

        password = self.browser.find_element_by_id('id_password')
        password.send_keys('Natalia123')

        btnLogin = self.browser.find_element_by_id('btnLogin')
        btnLogin.click()

        link = self.browser.find_element_by_id('addEstrategia')
        link.click()
        self.browser.implicitly_wait(1)

        name = self.browser.find_element_by_id('nameEstrategia')
        name.send_keys('PruebaTest')

        description = self.browser.find_element_by_id('description')
        description.send_keys('Descripcion de la estrategia')

        file_input = self.browser.find_element_by_id('imgInp')
        file_input.send_keys("C:\ideport-col.jpg")

        btnRevision = self.browser.find_element_by_id('btnRevision')
        btnRevision.click()

        a = self.browser.find_element(By.XPATH, '//a[text()="Estrategia Pedagógica - En Revisión"]')
        self.assertIn('Estrategia Pedagógica - En Revisión', a.text)
