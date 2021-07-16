from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage, Headers
import json
import os
import requests
import ast
app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template('index.html')
	
@app.route('/pan', methods = ['GET', 'POST'])
def pan():
    if request.method == 'GET':
        return render_template('pan.html')
    if request.method == 'POST':
        print(request.files)
        if request.files:   
            if request.files['file'].filename !="":
                print(1)
                file=request.files['file']
                filename = secure_filename(file.filename)
                print(filename)
                file.save(filename)
                response= requests.get('http://localhost:5000/panVerification', files = {'file':open(filename, 'rb')})
                print(type(response.text))
                d=ast.literal_eval(response.text)
                print(type(d))
                if d['valid']:
                        return "valid" + " number=" + str(d['number'])
                else:
                    return "invalid"

@app.route('/aadhar', methods = ['GET', 'POST'])
def aadhar():
    if request.method == 'GET':
        return render_template('aadhar.html')
    if request.method == 'POST':
            print(request.files)
            if request.files:   
                if request.files['file'].filename !="":
                    print(1)
                    file=request.files['file']
                    filename = secure_filename(file.filename)
                    print(filename)
                    file.save(filename)
                    response= requests.get('http://localhost:5000/aadharVerification', files = {'file':open(filename, 'rb')})
                    print(response.text)
                    d=ast.literal_eval(response.text)
                    print(type(d))
                    if d['valid']:
                        return "valid" + " number=" + str(d['number'])
                    else:
                        return "invalid"

if __name__ == '__main__':
    app.run(debug = True, port=8000)