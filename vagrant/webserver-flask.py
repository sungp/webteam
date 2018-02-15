from flask import Flask, render_template, request, redirect, jsonify,\
        url_for, flash
import cgi

app = Flask(__name__)

@app.route('/')
def showLink():
  htmlText = render_template('comingsoon.html');
  return htmlText; 

@app.route('/hello', methods=['GET', 'POST'])
def showHello():
  submitMsg = "";
  
  if request.method == 'POST':
    submitMsg = request.form['message'].strip();
  
  htmlText = render_template('hello.html', request = request, message = submitMsg);  
  print htmlText;
  return htmlText;

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
