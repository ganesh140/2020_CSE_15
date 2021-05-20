from flask import Flask, render_template, Response, request,flash,redirect,url_for
from werkzeug.utils import secure_filename
import os
import cv2
import aadharVerification
import panVerification
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aadhar", methods=['GET', 'POST'])
def aadhar():
    if request.method == 'POST':
        if request.files:   
            if request.files['file'].filename !="":
                print(1)
                file=request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    print(filename)
                    f=(os.path.join(app.config['UPLOAD_FOLDER']))
                    file.save(filename)
                    img=cv2.imread(filename)
                    a,num=aadharVerification.aadhar_auth_img(img)
                    if a:
                        return str(num) + " is Valid aadhar card" 
                    else:
                        return str(num) +" is Invalid aadhar card"
        else:
            number=request.form["number"]
            a,num=aadharVerification.aadhar_auth_number(number)
            if a:
                    return str(num) +" is Valid aadhar card"
            else:
                return str(num) + " is Invalid aadhar card"
    else:
        return render_template("aadhar.html")

@app.route("/pan", methods=['GET', 'POST'])
def pan():
    if request.method == 'POST':
        if request.files:   
            if request.files['file'].filename !="":
                print(1)
                file=request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    print(filename)
                    f=(os.path.join(app.config['UPLOAD_FOLDER']))
                    file.save(filename)
                    img=cv2.imread(filename)
                    a,num=panVerification.pan_auth_img(img)
                    if a:
                        return str(num) + " is Valid pancard" 
                    else:
                        return str(num) +" is Invalid pancard"
        else:
            number=request.form["number"]
            a,num=panVerification.pan_auth_number(number)
            if a:
                return str(num) +" is Valid pancard"
            else:
                return str(num) + " is Invalid pancard"
    else:
        return render_template("pancard.html")


if __name__ == '__main__':
  app.run(host="localhost",port=5000, debug=True)