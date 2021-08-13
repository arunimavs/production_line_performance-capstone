from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pickle
import pandas as pd
import sys
import numpy

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True


# Upload folder
UPLOAD_FOLDER = 'static/files/'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
# pickle_in = open("model.pkl","rb")
# classifier=pickle.load(pickle_in)
classifier=pickle.loads(open('model.pkl', 'rb').read())

@app.errorhandler(404)
def error404(error):
    message = "ERROR 404 OCCURED. Page Not Found. Please go the home page and try again"
    return render_template("error.html",message=message) # page not found

@app.errorhandler(405)
def error405(error):
    message = 'Error 405, Method Not Found'
    return render_template("error.html",message=message)

@app.errorhandler(500)
def error500(error):
   
    message='INTERNAL ERROR 500, Error occurs in the program'
    return render_template("error.html",message=message)


# Get the uploaded files
@app.route("/", methods=['GET','POST'])
def index():
      # get the uploaded file
    if request.method == "POST":
      uploaded_file = request.files['file']
      fileread=pd.read_csv(uploaded_file)
      if uploaded_file.filename != '':
           prediction = parseCSV(fileread)
           fileread = fileread[['Id','mindate','maxdate','min_time_station','max_time_station','min_Id_rev','min_Id','start_station','end_station']]
           fileread['Response']= numpy.where(prediction == 1, 'Faulty', 'Not faulty')
      return render_template('index.html', table = fileread.to_html(classes='data center m-a', header="true"),fileupload=True)

    else :
      return render_template('index.html',fileupload=False)


def parseCSV(filePath):
      prediction = classifier.predict(filePath.drop(['Id'],axis=1))
      print('labels****',prediction)
      return prediction;

      

if (__name__ == "__main__"):
     app.run(host='0.0.0.0',port = 5000)
