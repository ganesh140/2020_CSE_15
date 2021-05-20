#!/usr/bin/env python
# coding: utf-8

import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from chromedriver_py import binary_path
from google.cloud import vision
import io
import os
import re
import cv2


def pan_auth_img(img):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', img)
    img = encoded_image.tobytes()
    img = vision.Image(content=img)
    response = client.text_detection(image=img)
    texts = response.text_annotations[0].description.split("\n")
    l=[]
    for i in texts:
        if len(i)==10:
            regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
            # Compile the ReGex
            p = re.compile(regex)
            if(re.search(p, i)):
                l.append(i)
    url = "https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Registration/RegistrationHome.html?lang=eng"
    
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=binary_path,options=options)  
    driver.get(url)  
    # this is just to ensure that the page is loaded 
    time.sleep(1)  
    html = driver.page_source 
    s=Select(driver.find_element_by_id('userTypeSel'))
    s.select_by_visible_text('Individual')
    driver.find_element_by_id('UpdateContactDtls_0').click()
    time.sleep(1) 
    if len(l)==0:
        return False,"Photo uploaded"
    for i in l:
        print(i)
        inputElement = driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId")
        inputElement.send_keys(i)
        inputElement = driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName")
        inputElement.send_keys("KISHORE")
        driver.find_element_by_css_selector("input#contact_nriFlagN").click() 
        datefield = driver.find_element_by_id('dateField')
        datefield.click()
        datefield.send_keys("26021999")
        driver.find_element_by_id('continue').click()
        time.sleep(1)
        s="This PAN has already been registered"
        try:
            error=driver.find_element_by_class_name('error').text[:len(s)]
        except:
            print("valid")
            return True,i
        if(error!=s):
            print("invalid")
            driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId").clear()
            driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName").clear()
            return False,i
        else:
            print("valid")
            driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId").clear()
            driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName").clear()
            return True,i


def pan_auth_number(num):
    url = "https://www1.incometaxindiaefiling.gov.in/e-FilingGS/Registration/RegistrationHome.html?lang=eng"
    
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=binary_path,options=options)  
    driver.get(url)  
    # this is just to ensure that the page is loaded 
    time.sleep(1)  
    html = driver.page_source 
    s=Select(driver.find_element_by_id('userTypeSel'))
    s.select_by_visible_text('Individual')
    driver.find_element_by_id('UpdateContactDtls_0').click()
    time.sleep(1) 
    i=num
    inputElement = driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId")
    inputElement.send_keys(i)
    inputElement = driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName")
    inputElement.send_keys("KISHORE")
    driver.find_element_by_css_selector("input#contact_nriFlagN").click() 
    datefield = driver.find_element_by_id('dateField')
    datefield.click()
    datefield.send_keys("26021999")
    driver.find_element_by_id('continue').click()
    time.sleep(1)
    s="This PAN has already been registered"
    try:
        error=driver.find_element_by_class_name('error').text[:len(s)]
    except:
        print("valid")
        return True,i
    if(error!=s):
        print("invalid")
        driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId").clear()
        driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName").clear()
        return False,i
    else:
        print("valid")
        driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userId").clear()
        driver.find_element_by_id("RegistrationInvidualValidation_userProfile_userPersonalDetails_surName").clear()
        return True,i
# img=cv2.imread("D:/awesome/pan.jpeg")
# pan_auth_img(img)
# pan_auth_number("DTGPB7351")



