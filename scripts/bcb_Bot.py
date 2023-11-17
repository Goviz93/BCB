"""
    Author: GVR.
    Date: 19/10/2023
    Name: Project BCB.
    Customer:
"""

import io
import os
import random
import re
import logging
from bcb_Process import logger
from time import sleep, time
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
from scripts.customer_dataclass import Customer
from selenium.webdriver.common.by import By
from scripts.selenium_Browser import automatic_Browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

"""
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(lineno)d]: %(message)s')
logging.getLogger().setLevel(logging.INFO)
"""


# Timestamp.
def _timestamp():
    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    return timestamp


# Create folder if it doesn't exist.
def _createImageFolder():
    _folder = 'captchas'

    if os.path.exists(_folder):
        return os.path.abspath(_folder)
    else:
        os.mkdir(_folder)
        return os.path.abspath(_folder)


def _randomNumber():
    _numlist = random.sample(range(0, 9), 7)
    _num = ''.join(str(i) for i in _numlist)
    return _num


class BOT(automatic_Browser):

    def __init__(self, customer_object:Customer):
        super().__init__()

        self.URLs.update(
            {'Form_1': 'https://solicituddeatencion.bcb.gob.bo/bcb-solicitud-fe/pages/persona/persona.xhtml'
             })
        self.RiseBrowser()

        self.xpathDict = {
            'Atencion_arrow': "(//div[@class='ui-selectonemenu-trigger ui-state-default ui-corner-right'])[1]",
            'SantaCruz': "/html[1]/body[1]/div[10]/div[1]/ul[1]/li[4]",
            'NroDocumento': "/html[1]/body[1]/div[7]/div[1]/form[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div["
                            "2]/div[1]/div[1]/div[3]/span[1]/span[1]/input[1]",
            'Complemento': "/html[1]/body[1]/div[7]/div[1]/form[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div["
                           "2]/div[1]/div[1]/div[4]/span[1]/span[1]/input[1]",
            'Captcha_img': "//img[@id='persona_frmPrincipal:image']",
            'Captcha_textbox': "//input[@id='persona_frmPrincipal:codigoCaptcha']",
            'waitForm2': "//span[contains(text(),'En caso de no contar con esta documentación, su so')]"
        }

        self.xpath_form2_dict = dict()
        self.customer = customer_object
        logger.info(f"Customer Information -> {self.customer}")
        """
        self.customer = Customer(
            LastName="LUIS",
            SecondLastName="RODRIGUEZ",
            Name="NAYELI",
            Birthday="01/12/1990",
            NroDoc=_randomNumber(),
            Address="COTOCA LA ENCONADA",
            phone="77145212",
            email="Nay_123@gmail.com",
            Gender="F",
            USD="1000",
            Job="ESTUDIANTE UNIVERSITARIA",
            Source="AHORROS",
            Destiny="AHORROS" 
            )       
        """


        self.Token = None
        self.pattern = "(?<=nroDocumento)(.*)(?=_input)"
        self.keys_dict = {
            '0': Keys.NUMPAD0,
            '1': Keys.NUMPAD1,
            '2': Keys.NUMPAD2,
            '3': Keys.NUMPAD3,
            '4': Keys.NUMPAD4,
            '5': Keys.NUMPAD5,
            '6': Keys.NUMPAD6,
            '7': Keys.NUMPAD7,
            '8': Keys.NUMPAD8,
            '9': Keys.NUMPAD9
        }
        # self.workFlow()

    def workFlow(self):
        self.fill_form1()
        self.getElementScreenshot(self.getElementXPATH(self.xpathDict.get('Captcha_img')))
        self.wait_form2()
        self.getToken()
        self.updateXpath_dict()
        self.fill_form2()
        while True:
            self.wait_form3()
            self.fill_form3()
            sleep(2)
            self._captcha_2()


    def fill_form1(self):
        self.Bot_Browser.get(self.URLs.get('Form_1'))
        arrow = self.waitElementXPATH(self.xpathDict.get('Atencion_arrow'))
        arrow.click()
        santa = self.waitElementXPATH(self.xpathDict.get('SantaCruz'))
        santa.click()
        nroDocumento = self.waitElementXPATH(self.xpathDict.get('NroDocumento'))
        nroDocumento.click()
        nroDocumento.send_keys(self.customer.NroDoc)
        captcha_1 = self.waitElementXPATH(self.xpathDict.get('Captcha_textbox'))
        captcha_1.click()
        logger.info(f"Form 1 completed - Waiting for captcha")

    def fill_form2(self):
        start_time = time()
        self.push_button()
        self.window_maximize()
        sleep(0.08)

        self.find_boxes()

        _function_list = [
            self._paterno,
            self._materno,
            self._nombre,
            self._nacimiento,
            self._genero,
            self._direccion,
            self._celular,
            self._email,
            self._ocupacion,
            self._origen,
            self._destino,
            self._monto,
            self._captcha_2
        ]

        for fn in _function_list:
            try:
                fn()
            except StaleElementReferenceException as e:
                self.find_boxes()
                logging.error(f"Caught a StaleElementReferenceException. Retrying fn ->{fn}")
                fn()
            #sleep(_time)
        end_time = time()
        total_time = start_time - end_time
        print(f"Tiempo del form 2 -> {total_time}")

    def fill_form3(self):
        sub_form = self.waitElementXPATH("//div[@id='frmConfirmar:dlgConfirmar']")
        self.scrollDown_form(sub_form)
        self.push_terms()
        sleep(0.5)
        self.push_registry()

    def wait_form2(self):
            element = None
            while element is None:
                element = self.waitElementXPATH(self.xpathDict.get('waitForm2'))
            logger.info(f"Form 2 found and ready to be filled")

    def wait_form3(self):
        element = None
        while element is None:
            element = self.waitElementXPATH("//div[@id='frmConfirmar:dlgConfirmar']//span[@class='ui-icon ui-icon-extlink']")
        logger.info(f"Form 3 found and ready to be filled")

    def getToken(self):
        soup = BeautifulSoup(self.Bot_Browser.page_source, 'lxml')
        _label = soup.find('label', {'id': 'persona_frmPrincipal:j_idt44'})
        _rawPattern = _label.attrs.get('for')
        self.Token = re.findall(self.pattern, _rawPattern)
        logger.info(f"Token extracted -> {self.Token}")

    def updateXpath_dict(self):
        self.xpath_form2_dict = {
            'boton': ("//i[@class='pi pi-bars']"),
            'LastName': ("//input[@id='persona_frmPrincipal:primerApellido" + str(self.Token[0]) + "']"),
            'SecondLastName': ("//input[@id='persona_frmPrincipal:segundoApellido" + str(self.Token[0]) + "']"),
            'Name': ("//input[@id='persona_frmPrincipal:nombre" + str(self.Token[0]) + "']"),
            'Birthday': ("//input[@id='persona_frmPrincipal:calFecha" + str(self.Token[0]) + "_input']"),
            'Address': ("//input[@id='persona_frmPrincipal:direccion" + str(self.Token[0]) + "']"),
            'phone': ("//input[@id='persona_frmPrincipal:celular" + str(self.Token[0]) + "_input']"),
            'email': ("//input[@id='persona_frmPrincipal:correro" + str(self.Token[0]) + "']"),
            'Job': ("//input[@id='persona_frmPrincipal:rubro2" + str(self.Token[0]) + "_input']"),
            'Source': ("//input[@id='persona_frmPrincipal:origen" + str(self.Token[0]) + "']"),
            'Destiny': ("//input[@id='persona_frmPrincipal:destino" + str(self.Token[0]) + "']"),
            'USD': ("//input[@id='persona_frmPrincipal:monto" + str(self.Token[0]) + "_input']"),
            'Gender': ("//div[@id='persona_frmPrincipal:genero" + str(self.Token[0]) + "']"),
            'Captcha_2': "//input[@id='persona_frmPrincipal:codigoCaptcha2']"
        }
        self.ids_from2_dict = {
            'Gender_focus': ("persona_frmPrincipal:genero" + str(self.Token[0]) + "_focus"),
            'Gender_input': ("persona_frmPrincipal:genero" + str(self.Token[0]) + "_input"),
            'Gender_label': ("persona_frmPrincipal:genero" + str(self.Token[0]) + "_label"),
            'calendar': {'persona_frmPrincipal:calFecha' + str(self.Token[0])}
        }
        logger.info(f"XPATH Dictionary updated with form 2 xpaths")


    def find_boxes(self):
        self._Boxes = self.getElements_CLASS("ui-float-label")
        logger.info('def find_boxes -> Boxes found')

    def _paterno(self):
        _box_2 = self.waitElementXPATH(self.xpath_form2_dict.get('LastName'))
        self.focus(_box_2)
        logger.info('def _paterno -> Focus on LastName')
        #self._Boxes[2].click()
        #logging.info('click LastName')
        _box_2.send_keys(self.customer.LastName)
        logger.info(f'def _paterno -> Wrote LastName -> {self.customer.LastName}')



    def _materno(self):
        _box_3 = self.waitElementXPATH(self.xpath_form2_dict.get('SecondLastName'))
        self.focus(_box_3)
        logger.info('def _materno -> Focus on SecondLastName')
        #self._Boxes[3].click()
        #logging.info('click SecondLastName')
        _box_3.send_keys(self.customer.SecondLastName)
        logger.info(f'def _materno -> Wrote SecondLastName -> {self.customer.SecondLastName}')


    def _nombre(self):
        _box_4 = self.waitElementXPATH(self.xpath_form2_dict.get('Name'))
        self.focus(_box_4)
        logger.info('def _nombre -> Focus on Name')
        #self._Boxes[4].click()
        #logging.info('click Name')
        _box_4.send_keys(self.customer.Name)
        logger.info(f'def _nombre -> Wrote Name -> {self.customer.Name}')


    def _nacimiento(self):
        self.focus(self._Boxes[5])
        self._Boxes[5].click()
        logger.info('def _nacimiento -> Click on Birthday')

        _box5 = self.waitElementXPATH(self.xpath_form2_dict.get('Birthday'))
        self.focus(_box5)
        logger.info('def _nacimiento -> Focus on Birthday')


        _box5.send_keys(Keys.ESCAPE)
        #sleep(0.1)
        _box5.send_keys(Keys.SHIFT + Keys.HOME)
        #sleep(0.1)
        _box5.send_keys(Keys.DELETE)
        #sleep(0.1)
        logger.info('def _nacimiento -> Cleared default data from Birthday')

        _rawBirthday = self.customer.Birthday.replace('/','')

        for n in list(_rawBirthday):
            _box5.send_keys(self.keys_dict.get(n))
            logging.info(f'--- Birthday -> {self.keys_dict.get(n)}')
        logger.info('def _nacimiento -> Birthday Wrote')

    def _genero(self):
        gender_click = self.waitElementXPATH(self.xpath_form2_dict.get('Gender'))
        self.focus(gender_click)
        logger.info('def _genero -> Focus on gender_click')
        #gender_click.click()
        gender = self.Bot_Browser.find_element(by=By.ID, value=self.ids_from2_dict.get('Gender_focus'))
        self.focus(gender)
        logger.info('def _genero -> Focus on gender')
        if 'F' in self.customer.Gender:
            gender.send_keys('F')
        elif 'M' in self.customer.Gender:
            gender.send_keys('M')
        else:
            gender.send_keys('O')
        logger.info(f'def _genero -> Wrote {self.customer.Gender}')
        sleep(0.7)
        gender.send_keys(Keys.ENTER)



    def _direccion(self):
        self.focus(self._Boxes[6])
        logger.info('def _direccion -> Focus on self._Boxes[6]')
        #self._Boxes[6].click()
        _box_6 = self.waitElementXPATH(self.xpath_form2_dict.get('Address'))
        self.focus(_box_6)
        logger.info('def _direccion -> Focus on _box_6')
        _box_6.send_keys(self.customer.Address)
        logger.info(f'def _direccion -> Wrote {self.customer.Address}')


    def _celular(self):
        self.focus(self._Boxes[7])
        logger.info('def _celular -> Focus on self._Boxes[7]')
        #self._Boxes[7].click()
        #logging.info('click phone')
        _box_7 = self.waitElementXPATH(self.xpath_form2_dict.get('phone'))
        self.focus(_box_7)
        logger.info('def _celular -> Focus on _box_7')
        _box_7.send_keys(self.customer.phone)
        logger.info(f'def _celular -> Wrote {self.customer.phone}')


    def _email(self):
        self.focus(self._Boxes[8])
        logger.info('def _email -> Focus on self._Boxes[8]')
        #self._Boxes[8].click()
        #logging.info('click email')
        _box_8 = self.waitElementXPATH(self.xpath_form2_dict.get('email'))
        self.focus(_box_8)
        logger.info('def _email -> Focus on _box_8')
        logging.info('find email')
        _box_8.send_keys(self.customer.email)
        logger.info(f'def _email -> Wrote {self.customer.email}')


    def _ocupacion(self):
        _box_9 = self.waitElementXPATH(self.xpath_form2_dict.get('Job'))
        self.focus(_box_9)
        logger.info('def _ocupacion -> Focus on self._Boxes[9]')
        _box_9.send_keys(self.customer.Job)
        logging.info('write Job')
        logger.info(f'def _ocupacion -> Wrote {self.customer.Job}')
        self.waitElementXPATH('//li[@data-item-label]')
        options = self.getElements_XPATH('//li[@data-item-label]')
        for o in options:
            if o.accessible_name == self.customer.Job:
                o.click()
        logger.info(f'def _ocupacion -> Selected Option')


    def _origen(self):
        _box_10 = self.waitElementXPATH(self.xpath_form2_dict.get('Source'))
        self.focus(_box_10)
        logger.info('def _origen -> Focus on _box_10')
        _box_10.send_keys(self.customer.Source)
        logger.info(f'def _origen -> Wrote {self.customer.Source}')


    def _destino(self):
        _box_11 = self.waitElementXPATH(self.xpath_form2_dict.get('Destiny'))
        self.focus(_box_11)
        logger.info('def _destino -> Focus on _box_11')
        _box_11.send_keys(self.customer.Destiny)
        logger.info(f'def _destino -> Wrote {self.customer.Destiny}')


    def _monto(self):
        _box_12 = self.waitElementXPATH(self.xpath_form2_dict.get('USD'))
        self.focus(_box_12)
        logger.info('def _monto -> Focus on _box_12')
        _box_12.send_keys(self.customer.USD)
        logger.info(f'def _monto -> Wrote {self.customer.USD}')

        print("Proceso Completado")


    def _captcha_2(self):
        self.scrollDown()
        self.scrollDown()
        _captcha_2 = self.waitElementXPATH(self.xpath_form2_dict.get('Captcha_2'))
        self.focus(_captcha_2)
        _captcha_2.click()


    def getElementScreenshot(self, web_element):
        _web_element = web_element
        _image = _web_element.screenshot_as_png
        _image_stream = io.BytesIO(_image)
        _image_Pil = Image.open(_image_stream)
        _image_Pil.save(_createImageFolder() + '/' + str(_timestamp()) + '.png')
        logger.info(f"Captcha saved")


    def push_button(self):
        boton = self.waitElementXPATH(self.xpath_form2_dict.get('boton'))
        boton.click()

    def push_terms(self):
        boton = self.waitElementXPATH("//div[@class='ui-chkbox-box ui-widget ui-corner-all ui-state-default']")
        boton.click()

    def push_registry(self):
        boton = self.waitElementXPATH("//span[normalize-space()='Registrar']")
        boton.click()
