from google.cloud import vision
import os
import re
import cv2

def resize_aadhar_mar(image,height,width):
    height=int(image.shape[0]//(image.shape[1]/width))
    if width>image.shape[1]:
        interpolation=cv2.INTER_LINEAR
    else:
        interpolation=cv2.INTER_CUBIC

    resized = cv2.resize(image, (width,height),interpolation=interpolation)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', resized)
    img = encoded_image.tobytes()
    img = vision.Image(content=img)
    response = client.text_detection(image=img)
    texts = response.text_annotations[0].description.split("\n")
    print(texts)
    l=[]
    regex = ("^[2-9]{1}[0-9]{3}\\" +"s[0-9]{4}\\s[0-9]{4}$")
    p = re.compile(regex)
    for i in texts:
        if(re.search(p, i)):
            l.append(i)
            print(i)
    if (len(l)!=0):
        success, encoded_image = cv2.imencode('.jpg', image)
        img = encoded_image.tobytes()
        img = vision.Image(content=img)
        response = client.text_detection(image=img)
        original_texts = response.text_annotations[0].description.split("\n")
        print(original_texts)
        match=0
        for i in original_texts:
            if i in texts:
                match+=1
        if match>3:
            print("File resized to",resized.shape)
            return True,resized
        else:
            print("size not appropriate")
        return False,None
    else:
        print("size not appropriate")
        return False,None

def resize_aadhar_hard(image,height,width):
    if width>image.shape[1]:
        interpolation=cv2.INTER_LINEAR
    else:
        interpolation=cv2.INTER_CUBIC
    resized = cv2.resize(image, (width,height),interpolation=interpolation)   
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"
    client = vision.ImageAnnotatorClient()
    success, encoded_image = cv2.imencode('.jpg', resized)
    img = encoded_image.tobytes()
    img = vision.Image(content=img)
    response = client.text_detection(image=img)
    texts = response.text_annotations[0].description.split("\n")
    print(texts)
    l=[]
    regex = ("^[2-9]{1}[0-9]{3}\\" +"s[0-9]{4}\\s[0-9]{4}$")
    p = re.compile(regex)
    for i in texts:
        if(re.search(p, i)):
            l.append(i)
            print(i)
    if (len(l)!=0):
        success, encoded_image = cv2.imencode('.jpg', image)
        img = encoded_image.tobytes()
        img = vision.Image(content=img)
        response = client.text_detection(image=img)
        original_texts = response.text_annotations[0].description.split("\n")
        print(original_texts)
        match=0
        for i in original_texts:
            if i in texts:
                match+=1
        if match>3:
            print("File resized to",resized.shape)
            return True,resized
        else:
            print("size not appropriate")
        return False,None
    else:
        print("size not appropriate")
        return False,None