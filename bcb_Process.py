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
from time import sleep, time
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
from customer_dataclass import Customer
from selenium.webdriver.common.by import By
from selenium_Browser import automatic_Browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(lineno)d]: %(message)s')
logging.getLogger().setLevel(logging.INFO)





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

    def __init__(self):
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
        self.openform1()
        self.getElementScreenshot(self.getElementXPATH(self.xpathDict.get('Captcha_img')))
        self.waitform2()
        self.getToken()
        self.updateXpath_dict()
        self.fill_form2()


    def openform1(self):
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


    def waitform2(self):
        self.waitElementXPATH(self.xpathDict.get('waitForm2'))

    def getToken(self):
        soup = BeautifulSoup(self.Bot_Browser.page_source, 'lxml')
        _label = soup.find('label', {'id': 'persona_frmPrincipal:j_idt44'})
        _rawPattern = _label.attrs.get('for')
        self.Token = re.findall(self.pattern, _rawPattern)

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

    def fill_form2(self):
        start_time = time()
        self.push_button()
        self.window_maximize()
        sleep(0.1)

        self.find_boxes()

        _function_list = [
            self._paterno,
            self._materno,
            self._nombre,
            self._nacimiento,
            self._genero,
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

        #_time = 0.1
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



    def find_boxes(self):
        self._Boxes = self.getElements_CLASS("ui-float-label")
        logging.info('Boxes found')

    def _paterno(self):
        _box_2 = self.waitElementXPATH(self.xpath_form2_dict.get('LastName'))
        self.focus(_box_2)
        logging.info('find LastName')
        self._Boxes[2].click()
        logging.info('click LastName')
        _box_2.send_keys(self.customer.LastName)
        logging.info('write LastName')


    def _materno(self):
        _box_3 = self.waitElementXPATH(self.xpath_form2_dict.get('SecondLastName'))
        self.focus(_box_3)
        logging.info('find SecondLastName')
        self._Boxes[3].click()
        logging.info('click SecondLastName')
        _box_3.send_keys(self.customer.SecondLastName)
        logging.info('write SecondLastName')


    def _nombre(self):
        _box_4 = self.waitElementXPATH(self.xpath_form2_dict.get('Name'))
        self.focus(_box_4)
        logging.info('find Name')
        self._Boxes[4].click()
        logging.info('click Name')
        _box_4.send_keys(self.customer.Name)
        logging.info('write Name')


    def _nacimiento(self):
        self.focus(self._Boxes[5])
        self._Boxes[5].click()
        logging.info('click Birthday')
        
        _box5 = self.waitElementXPATH(self.xpath_form2_dict.get('Birthday'))
        self.focus(_box5)
        logging.info('write Birthday')

        _box5.send_keys(Keys.ESCAPE)
        #sleep(0.1)
        _box5.send_keys(Keys.SHIFT + Keys.HOME)
        #sleep(0.1)
        _box5.send_keys(Keys.DELETE)
        #sleep(0.1)

        _rawBirthday = self.customer.Birthday.replace('/','')
        logging.info(f'--- Birthday -> {_rawBirthday}')
        for n in list(_rawBirthday):
            _box5.send_keys(self.keys_dict.get(n))
            logging.info(f'--- Birthday -> {self.keys_dict.get(n)}')


    def _genero(self):
        gender_click = self.waitElementXPATH(self.xpath_form2_dict.get('Gender'))
        self.focus(gender_click)
        gender_click.click()
        #sleep(0.05)
        gender = self.Bot_Browser.find_element(by=By.ID, value=self.ids_from2_dict.get('Gender_focus'))
        self.focus(gender)

        if 'F' in self.customer.Gender:
            gender.send_keys('F')
        elif 'M' in self.customer.Gender:
            gender.send_keys('M')
        else:
            gender.send_keys('O')
        sleep(0.1)
        gender.send_keys(Keys.ENTER)


    def _direccion(self):
        self.focus(self._Boxes[6])
        self._Boxes[6].click()
        logging.info('click Address')
        _box_6 = self.waitElementXPATH(self.xpath_form2_dict.get('Address'))
        self.focus(_box_6)
        logging.info('find Address')
        _box_6.send_keys(self.customer.Address)
        logging.info('write Address')


    def _celular(self):
        self.focus(self._Boxes[7])
        self._Boxes[7].click()
        logging.info('click phone')
        _box_7 = self.waitElementXPATH(self.xpath_form2_dict.get('phone'))
        self.focus(_box_7)
        logging.info('find phone')
        _box_7.send_keys(self.customer.phone)
        logging.info('write phone')


    def _email(self):
        self.focus(self._Boxes[8])
        self._Boxes[8].click()
        logging.info('click email')
        _box_8 = self.waitElementXPATH(self.xpath_form2_dict.get('email'))
        self.focus(_box_8)
        logging.info('find email')
        _box_8.send_keys(self.customer.email)
        logging.info('write email')


    def _ocupacion(self):
        _box_9 = self.waitElementXPATH(self.xpath_form2_dict.get('Job'))
        self.focus(_box_9)
        logging.info('find Job')
        _box_9.send_keys(self.customer.Job)
        logging.info('write Job')
        #sleep(0.2)
        self.waitElementXPATH('//li[@data-item-label]')
        options = self.getElements_XPATH('//li[@data-item-label]')
        for o in options:
            if o.accessible_name == self.customer.Job:
                o.click()


    def _origen(self):
        _box_10 = self.waitElementXPATH(self.xpath_form2_dict.get('Source'))
        self.focus(_box_10)
        logging.info('find Source')
        _box_10.send_keys(self.customer.Source)
        logging.info('write Source')


    def _destino(self):
        _box_11 = self.waitElementXPATH(self.xpath_form2_dict.get('Destiny'))
        self.focus(_box_11)
        logging.info('find Destiny')
        _box_11.send_keys(self.customer.Destiny)
        logging.info('write Destiny')


    def _monto(self):
        _box_12 = self.waitElementXPATH(self.xpath_form2_dict.get('USD'))
        self.focus(_box_12)
        logging.info('find USD')
        _box_12.send_keys(self.customer.USD)
        logging.info('write USD')

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


    def push_button(self):
        boton = self.waitElementXPATH(self.xpath_form2_dict.get('boton'))
        boton.click()


