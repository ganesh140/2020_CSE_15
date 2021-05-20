#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


def aadhar_auth_img(img)  :
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', img)
    img = encoded_image.tobytes()
    img = vision.Image(content=img)
    response = client.text_detection(image=img)
    texts = response.text_annotations[0].description.split("\n")
    l=[]
    regex = ("^[2-9]{1}[0-9]{3}\\" +"s[0-9]{4}\\s[0-9]{4}$")
    p = re.compile(regex)
    for i in texts:
        if(re.search(p, i)):
            l.append(i)
            print(i)
    url = "https://resident.uidai.gov.in/verify"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=binary_path,options=options)  
    driver.get(url)  
    time.sleep(1)  
    html = driver.page_source 
    if(len(l)==0):
        return False,"Photo uploaded"
    for i in l:
        inputElement = driver.find_element_by_id("uidno")
        inputElement.send_keys(i)
        output= driver.find_element_by_class_name("errormsgClass")
        if(output.get_attribute("style")=="display: block;"):
            print("invalid",i)
        else:
            print("valid",i)
            driver.find_element_by_id("uidno").clear()
            return True,i
        driver.find_element_by_id("uidno").clear()
    return False,i


def aadhar_auth_number(num)  :
    if len(num)!=12:
        return False,num
    url = "https://resident.uidai.gov.in/verify"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path=binary_path,options=options)  
    driver.get(url)  
    time.sleep(1)  
    i=num
    html = driver.page_source 
    inputElement = driver.find_element_by_id("uidno")
    inputElement.send_keys(i)
    output= driver.find_element_by_class_name("errormsgClass")
    if(output.get_attribute("style")=="display: block;"):
        print("invalid",i)
    else:
        print("valid",i)
        return True,i
    driver.find_element_by_id("uidno").clear()
    return False,i


# img=cv2.imread("D:/awesome/aadhar.jpg")
# aadhar_auth_img(img)
# aadhar_auth_number("123412341234")





