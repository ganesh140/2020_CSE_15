import re
from flask import Flask, render_template, Response, request,flash,redirect,url_for
from flask.helpers import send_file
from werkzeug.utils import secure_filename
import os
import cv2
import aadharVerification
import panVerification
import panResize 
import aadharResize
import numpy
import reduceSize


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aadharVerification", methods=['GET'])
def aadhar():
    try:
        if request.files:   
            if request.files['file'].filename !="":
                print(1)
                file=request.files['file'].read()
                #convert string data to numpy array
                npimg = numpy.fromstring(file, numpy.uint8)

                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                a,num=aadharVerification.aadhar_auth_img(img)
                if a:
                    return Response(str({'number': str(num) ,'valid':True}),status=200,mimetype='application/json')
                else:
                    return Response(str({'number': '', 'valid':False}),status=200,mimetype='application/json')
        else:
            number=request.form["number"]
            a,num=aadharVerification.aadhar_auth_number(number)
            if a:
                    return Response(str({'number': str(num) ,'valid':True}),status=200,mimetype='application/json')
            else:
                return Response(str({'number': '', 'valid':False}),status=200,mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(str({'number': '', 'valid':''}),status=403,mimetype='application/json')


@app.route("/panVerification", methods=['GET'])
def pan():
    try:
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                a,num=panVerification.pan_auth_img(img)
                if a:
                    return Response(str({'number': str(num) ,'valid':True}),status=200,mimetype='application/json')
                else:
                    return Response(str({'number': '', 'valid':False}),status=200,mimetype='application/json')
        else:
            number=request.form["number"]
            a,num=panVerification.pan_auth_number(number)
            if a:
                return Response(str({'number': str(num) ,'valid':True}),status=200,mimetype='application/json')
            else:
                return Response(str({'number': '', 'valid':False}),status=200,mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(str({'number':'','isvalid':''}),status=400,mimetype='application/json')


@app.route("/panResizeMAR",methods=["GET"])
def panresizeMAR():
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                height=int(request.form['height'])
                width=int(request.form['width'])
                a=panResize.resize_pan_mar(img,height,width)
                if a[0]:
                    cv2.imwrite("resized.jpeg",a[1])
                    return send_file("resized.jpeg",mimetype='image/jpeg') 
                else:
                    return "Inappropiate size"


@app.route("/panResizeHard",methods=["GET"])
def panresizehard():
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                height=int(request.form['height'])
                width=int(request.form['width'])
                a=panResize.resize_pan_hard(img,height=height,width=width)
                if a[0]:
                    cv2.imwrite("resized.jpeg",a[1])
                    return send_file("resized.jpeg",mimetype='image/jpeg') 
                else:
                    return "Inappropiate size"


@app.route("/aadharResizeHard",methods=["GET"])
def aadhar_resize_hard():
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                height=int(request.form['height'])
                width=int(request.form['width'])
                a=aadharResize.resize_aadhar_hard(img,height=height,width=width)
                if a[0]:
                    cv2.imwrite("resized.jpeg",a[1])
                    return send_file("resized.jpeg",mimetype='image/jpeg') 
                else:
                    return "Inappropiate size"


@app.route("/aadharResizeMAR",methods=["GET"])
def aadhar_resize_mar():
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                height=int(request.form['height'])
                width=int(request.form['width'])
                a=aadharResize.resize_aadhar_mar(img,height=height,width=width)
                if a[0]:
                    cv2.imwrite("resized.jpeg",a[1])
                    return send_file("resized.jpeg",mimetype='image/jpeg') 
                else:
                    return "Inappropiate size"


@app.route("/reduceSize",methods=["GET"])
def reduce():
        if request.files:   
            if request.files['file'].filename !="":
                file=request.files['file'].read()
                npimg = numpy.fromstring(file, numpy.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                a=reduceSize.reduce_storeage(img)
                if a:
                    return send_file("reduced.jpeg",mimetype='image/jpeg') 
                else:
                    return ""

if __name__ == '__main__':
  app.run(host="localhost",port=5000, debug=True)