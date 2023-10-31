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
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass
from selenium_Browser import automatic_Browser
from selenium.webdriver.common.keys import Keys


logging.basicConfig(level=logging.INFO,  format='%(asctime)s [%(lineno)d]: %(message)s')
logging.getLogger().setLevel(logging.INFO)


@dataclass
class Customer:
    LastName: str
    SecondLastName: str
    Name: str
    Birthday: str
    Gender: str
    phone: str
    NroDoc: str
    Address: str
    email: str
    USD: str
    Job: str
    Source: str
    Destiny: str


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
    _numlist = random.sample(range(0,9),7)
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
            NroDoc= _randomNumber(),
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
        #self.workFlow()



    def workFlow(self):
        self.openform1()
        self.getElementScreenshot(self.getElementXPATH(self.xpathDict.get('Captcha_img')))
        self.waitform2()
        self.getToken()
        self.updateXpath_dict()
        self.Fill_form2()


    def openform1(self):
        self.Bot_Browser.get(self.URLs.get('Form_1'))
        arrow = self.waitElementXPATH(self.xpathDict.get('Atencion_arrow'))
        arrow.click()
        santa = self.waitElementXPATH(self.xpathDict.get('SantaCruz'))
        santa.click()
        nroDocumento = self.waitElementXPATH(self.xpathDict.get('NroDocumento'))
        nroDocumento.click()
        nroDocumento.send_keys(self.customer.NroDoc)

    def waitform2(self):
        self.waitElementXPATH(self.xpathDict.get('waitForm2'))


    def getToken(self):
        soup = BeautifulSoup(self.Bot_Browser.page_source, 'lxml')
        _label = soup.find('label', {'id': 'persona_frmPrincipal:j_idt44'})
        _rawPattern = _label.attrs.get('for')
        self.Token = re.findall(self.pattern, _rawPattern)


    def updateXpath_dict(self):
        self.xpath_form2_dict = {
            'LastName': ("//input[@id='persona_frmPrincipal:primerApellido" + str(self.Token[0]) + "']"),
            'SecondLastName': ("//input[@id='persona_frmPrincipal:segundoApellido" + str(self.Token[0]) + "']"),
            'Name': ("//input[@id='persona_frmPrincipal:nombre" + str(self.Token[0]) + "']"),
            'Birthday': ("//input[@id='persona_frmPrincipal:calFecha" + str(self.Token[0]) + "']"),
            'Address': ("//input[@id='persona_frmPrincipal:direccion" + str(self.Token[0]) + "']"),
            'phone': ("//input[@id='persona_frmPrincipal:celular" + str(self.Token[0]) + "_input']"),
            'email': ("//input[@id='persona_frmPrincipal:correro" + str(self.Token[0]) + "']"),
            'Job': ("//input[@id='persona_frmPrincipal:rubro2" + str(self.Token[0]) + "_input']"),
            'Source': ("//input[@id='persona_frmPrincipal:origen" + str(self.Token[0]) + "']"),
            'Destiny': ("//input[@id='persona_frmPrincipal:destino" + str(self.Token[0]) + "']"),
            'USD': ("//input[@id='persona_frmPrincipal:monto" + str(self.Token[0]) + "_input']"),
            'Gender': ("//div[@id='persona_frmPrincipal:genero" + str(self.Token[0]) + "']")
        }

    def Fill_form2(self):

        _Boxes = self.getElements_CLASS("ui-float-label")
        logging.info('Boxes found')

        self.scrollDown()
        logging.info('scrolled down')

        #Paterno:
        _box_2 = self.waitElementXPATH(self.xpath_form2_dict.get('LastName'))
        logging.info('find LastName')
        _Boxes[2].click()
        logging.info('click LastName')
        _box_2.send_keys(self.customer.LastName)
        logging.info('write LastName')

        #Materno:
        _box_3 = self.waitElementXPATH(self.xpath_form2_dict.get('SecondLastName'))
        logging.info('find SecondLastName')
        _Boxes[3].click()
        logging.info('click SecondLastName')
        _box_3.send_keys(self.customer.SecondLastName)
        logging.info('write SecondLastName')

        #Nombre:
        _box_4 = self.waitElementXPATH(self.xpath_form2_dict.get('Name'))
        logging.info('find Name')
        _Boxes[4].click()
        logging.info('click Name')
        _box_4.send_keys(self.customer.Name)
        logging.info('write Name')

        #Nacimiento:
        """
        _box_6 = self.waitElementXPATH(self.xpath_form2_dict.get('Birthday'))
        logging.info('find Birthday')
        
        _box_6.send_keys(self.customer.Birthday)
        logging.info('write Birthday')
        """

        self.scrollDown()
        logging.info('scroll down')

        #Direccion:
        _box_6 = self.waitElementXPATH(self.xpath_form2_dict.get('Address'))
        logging.info('find Address')
        _Boxes[6].click()
        logging.info('click Address')
        _box_6.send_keys(self.customer.Address)
        logging.info('write Address')

        #Celular:
        _box_7 = self.waitElementXPATH(self.xpath_form2_dict.get('phone'))
        logging.info('find phone')
        _Boxes[7].click()
        logging.info('click phone')
        _box_7.send_keys(self.customer.phone)
        logging.info('write phone')

        #email:
        _box_8 = self.waitElementXPATH(self.xpath_form2_dict.get('email'))
        logging.info('find email')
        _Boxes[8].click()
        logging.info('click email')
        _box_8.send_keys(self.customer.email)
        logging.info('write email')

        self.scrollDown()
        logging.info('scroll down')

        #Job:
        _box_9 = self.waitElementXPATH(self.xpath_form2_dict.get('Job'))
        logging.info('find Job')
        _Boxes[9].click()
        logging.info('click Job')
        _box_9.send_keys(self.customer.Job)
        logging.info('write Job')

        self.scrollDown()

        #Source:
        _box_10 = self.waitElementXPATH(self.xpath_form2_dict.get('Source'))
        logging.info('find Source')
        #_Boxes[10].click()
        logging.info('click Source')
        _box_10.send_keys(self.customer.Source)
        logging.info('write Source')
        _box_10.send_keys(Keys.TAB)
        logging.info('write Source TAB')


        self.scrollDown()
        logging.info('scroll down')

        #Destiny:
        _box_11 = self.waitElementXPATH(self.xpath_form2_dict.get('Destiny'))
        logging.info('find Destiny')
        #_Boxes[11].click()
        logging.info('click Destiny')
        _box_11.send_keys(self.customer.Destiny)
        logging.info('write Destiny')

        #USD:
        _box_12 = self.waitElementXPATH(self.xpath_form2_dict.get('USD'))
        logging.info('find USD')
        _Boxes[12].click()
        logging.info('click USD')
        _box_12.send_keys(self.customer.USD)
        logging.info('write USD')

        input('Finalizar?')


    def getElementScreenshot(self, web_element):
        _web_element = web_element
        _image = _web_element.screenshot_as_png
        _image_stream = io.BytesIO(_image)
        _image_Pil = Image.open(_image_stream)
        _image_Pil.save(_createImageFolder() + '/' + str(_timestamp()) + '.png')






