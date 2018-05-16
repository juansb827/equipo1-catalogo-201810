# encoding: utf-8
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FunctionalTest(TestCase):

    @classmethod
    def setUpClass(inst):
        inst.browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
        inst.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(inst):
        inst.browser.quit()



    def test_detalle_miembro(self):
        # Navega hasta la pagina de miembro
        #TODO: ir a la pagina del equipo y hacer click en un asesor
        self.browser.get("http://localhost:8000/catalogo/equipo/detalle/")

        # Verifica que este el nombre
        nombre = self.browser.find_element_by_id('name')
        self.assertTrue( nombre)

        # Verifica que este la descripcion
        descripcion = self.browser.find_element_by_id('description')
        self.assertTrue(descripcion)

        # Verifica que tenga herramientas
        herramientas = self.browser.find_element_by_id('tools').find_elements_by_tag_name('li')
        self.assertTrue( len(herramientas) > 0, "El asesor deberia tener herramientas")

        # Verifica que cada herramienta tenga el nombre
        herramientaVacia = False
        for herr in herramientas:
            if not herr.text:
                herramientaVacia = True
                break

        self.assertTrue( not herramientaVacia, "El nombre de la herramienta no deberia estar vacio")

        # Verifica que tenga areas de experiencia
        areas = self.browser.find_element_by_id('experience').find_elements_by_tag_name('li')
        self.assertTrue(len(areas) > 0, "El asesor deberia tener areas de experiencia")

        # Verifica que las areas de experiencia tengan nombres
        areaVacia = False
        for area in areas:
            if not area.text:
                areaVacia = True
                break
        self.assertTrue(not areaVacia, "El nombre de la area de experiencia no deberia estar vacio")

        # Verifica que tenga proyectos
        proyectos = self.browser.find_element_by_id('projects').find_elements_by_tag_name('li')
        self.assertTrue(len(proyectos) > 0, "El asesor deberia tener proyectos")

        # Verifica que los proyectos tengan nombre y la contribucion del asesor al proyecto
        proyectoVacio = False
        for proyecto in proyectos:
            nombre = proyecto.find_element_by_class_name("project-name")
            contribucion = proyecto.find_element_by_class_name("project-des")
            if (not nombre.text) or (not contribucion.text):
                proyectoVacio = True
                break
        self.assertTrue(not proyectoVacio, "El nombre del proyecto y la contribucion del asesor sobre este no deberian estar vacios")

        # Verifica que el asesor tenga email
        email = self.browser.find_element_by_id('email')
        self.assertTrue( email, "El asesor deberia tener email")

        # Verifica que el asesor tenga extension
        extension = self.browser.find_element_by_id('extension')
        self.assertTrue(extension, "El asesor deberia tener extension")

    def test_detalle_herramientas(self):
        # Navega hasta la pagina principal
        # TODO: ir a la pagina del equipo y hacer click en un asesor

        self.browser = webdriver.Chrome(executable_path=r"chromedriver.exe")
        self.browser.get("http://localhost:8000/catalogo/")
        select = Select(self.browser.find_element_by_id("idCategoria"))
        select.select_by_visible_text('Herramienta')

        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "card")
                )
            )
            buscar = self.browser.find_element_by_id('btnBuscar')
            buscar.send_keys("\n")
            herramienta = self.browser.find_element_by_id('http://localhost:8000/catalogo/verItem/?type=2&code=102&ver=2')
            herramienta.send_keys("\n")

            # Verifica que este el nombre
            nombre = self.browser.find_element_by_id('name1')
            self.assertTrue(nombre)

            # Verifica que este la descripcion
            descripcion = self.browser.find_element_by_id('description1')
            self.assertTrue(descripcion)

        finally:
            self.browser.implicitly_wait(100)
            self.browser.quit()







