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
    print(texts)
    l=[]
    for i in texts:
        if len(i)==10:
            regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
            # Compile the ReGex
            p = re.compile(regex)
            if(re.search(p, i)):
                l.append(i)
 
    url = "https://eportal.incometax.gov.in/iec/foservices/#/pre-login/register"
    
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=binary_path,options=options)  
    driver.get(url)  
    # this is just to ensure that the page is loaded 
    time.sleep(1)    
    html = driver.page_source
    for i in l:
        inputElement=driver.find_element_by_class_name('mat-input-element')
        inputElement.send_keys(i)
        driver.find_elements_by_class_name("normal-button-primary")[1].click()
        html=driver.page_source
        while(driver.page_source==html):
            time.sleep(3)

        try:
            error=driver.find_element_by_class_name("mat-error1").text
            if(error=="Error : The PAN entered does not exist. Please retry."):
                print("invalid")
                return False,1
            else:
                print("valid")
                return True,i
        except:
            try:
                success=driver.find_elements_by_class_name("body-2-text")[2]
                print("valid")
                return True,i
            except:
                print("invalid")
                return False,1


def pan_auth_number(num):
    regex = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
    p = re.compile(regex)
    if(re.search(p, num)):

        url = "https://eportal.incometax.gov.in/iec/foservices/#/pre-login/register"
        # initiating the webdriver. Parameter includes the path of the webdriver. 
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path=binary_path,options=options)   
        driver.get(url)  
        # this is just to ensure that the page is loaded 
        time.sleep(1)  
        html = driver.page_source 
        inputElement=driver.find_element_by_class_name('mat-input-element')
        inputElement.send_keys(num)
        driver.find_elements_by_class_name("normal-button-primary")[1].click()
        html=driver.page_source
        while(driver.page_source==html):
            time.sleep(3)
        
        try:
            error=driver.find_element_by_class_name("mat-error1").text
            if(error=="Error : The PAN entered does not exist. Please retry."):
                print("invalid")
                return False,1
            else:
                print("valid")
                return True,num
        except:
            try:
                success=driver.find_elements_by_class_name("body-2-text")[2]
                print("valid")
                return True,num
            except:
                print("invalid")
                return False,1
    else:
        print("invalid")
        return False,1



