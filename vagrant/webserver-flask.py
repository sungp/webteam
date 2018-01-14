from flask import Flask, render_template, request, redirect, jsonify,\
        url_for, flash
import cgi

app = Flask(__name__)

@app.route('/')
def showLink():
  output = ""
  output += "<html><body>"
  output += "<h1>Where would you like to go</h1>"
  output += "<a href = '/hello'> <h3> Hello </h3> </a>"
  output += "</body></html>"
  return output;

@app.route('/hello', methods=['GET', 'POST'])
def showHello():
  output = ""
  output += "<html><body>"
  output += "<h1>Hello!</h1>"

  if request.method == 'POST':
    output += " <h2> Okay, how about this: </h2>"
    output += "<h1> %s </h1>" % request.form['message'].strip() 
  output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
  output += "</body></html>"
  return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
