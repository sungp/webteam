
from flask import Flask, render_template, request, redirect, jsonify,\
        url_for, flash
import cgi

app = Flask(__name__)

@app.route('/')
def showLink():
  htmlText = render_template('main.html');
  return htmlText; 

@app.route('/hello', methods=['GET', 'POST'])
def showHello():
  submitMsg = "";
  field = "hello";

  if request.method == 'POST':
    submitMsg = request.form['message'].strip();
  
  htmlText = render_template('common.html', request = request, message = submitMsg, field = field);  
  print htmlText;
  return htmlText;

@app.route('/happy123', methods=['GET', 'POST'])
def showHappy123():
  message = "";
  landingpage = "";
  field = 'happy123'

  if request.method == 'POST':
    dictval = request.form.to_dict()
    print dictval
    message = dictval['message']
    landingpage = dictval['landingpage']
    write_file(message, landingpage)

  htmlText = render_template('common.html', request = request, message = message, landingpage = landingpage, field = field);  
  print htmlText;
  return htmlText;


@app.route('/gloomy321', methods=['GET', 'POST'])
def showGloomy321():
  message = "";
  landingpage = "";
  field = "gloomy321";

  if request.method == 'POST':
    dictval = request.form.to_dict()
    print dictval
    message = dictval['message']
    landingpage = dictval['landingpage']
    write_file(message, landingpage)

  htmlText = render_template('common.html', request = request, message = message, landingpage = landingpage, field = field);  
  print htmlText;
  return htmlText;

@app.route('/robobook', methods=['GET'])
def showRoboBook():
  content = ""
  content = read_file()

  htmlText = render_template('robobook.html', request = request, content = content);  
  print htmlText;
  return htmlText;

def write_file(message, landingpagecontent):
    print 'user printed ' + message
    fh = open("messages.txt","a")
    fh.write(message + " , " + landingpagecontent)
    fh.write('\n')
    fh.close()

def read_file():
    fh = open("messages.txt","r")
    lines = fh.readlines()
    print lines

    content = {}
    user = ""
    url = ""

    for line in lines:
      data = line.split(",") 
      user = data[0].strip()
      url = data[1].strip()

      content[user] = url

    fh.close()
    return content


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
