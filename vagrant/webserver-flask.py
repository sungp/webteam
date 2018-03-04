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

@app.route('/userform', methods=['GET', 'POST'])
def showUserFormPage():
  positive = "";
  negative = "";
  helper = "";
  shout = "";

  successMsg = 'Thank you for your submission!';
  
  if request.method == 'POST':
    positive = request.form['positive'].strip();
    negative = request.form['negative'].strip();
    helper = request.form['helper'].strip();
    shout = request.form['shout'].strip();

    print "positive : " + positive
    print "negative : " + negative
    print "helper : " + helper
    print "shout : " + shout 
  
  htmlText = render_template('userform.html', request = request, positive = positive, negative = negative, helper = helper, shout = shout, successMsg = successMsg);  
  return htmlText;

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
