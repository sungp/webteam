
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
  output += "<a href = '/happy123'> <h3> Happy123 </h3> </a>"
  output += "<a href = '/gloomy321'> <h3> Gloomy321 </h3> </a>"
  output += "<a href = '/robobook'> <h3> RoboBook </h3> </a>"
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

@app.route('/world', methods=['GET'])
def showWorld():
  output = ""
  output += "<html><body>Hello World Now!</body></html>"
  return output

@app.route('/message', methods=['GET'])
def showMessage():
  output = ""
  output += "<html>"
  output += "<body>"
  output += "<h1>Hello!</h1>"
  output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
  output += "<h2>What would you like me to say?</h2>"
  output += "<input name=\"message\" type=\"text\" >"
  output += "<input type=\"submit\" value=\"Submit\">"
  output += "</form>"
  output += "</body>"
  output += "</html>" 
  return output

@app.route('/message2', methods=['GET'])
def showMessage2():
  output = ""
  output += "<html>"
  output += "<body>"
  output += "<h1>What is your message</h1>"
  output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
  output += "<h2>What would you like me to say?</h2>"
  output += "<input name=\"message\" type=\"text\" >"
  output += "<input type=\"submit\" value=\"Submit\">"
  output += "</form>"
  output += "</body>"
  output += "</html>" 
  return output

@app.route('/happy123', methods=['GET', 'POST'])
def showHappy123():
  if request.method == 'POST':
    dictval = request.form.to_dict()
    print dictval
    messagecontent = dictval['message']
    landingpagecontent = dictval['landingpage']
    write_file(messagecontent, landingpagecontent)

    output = ""
    output += "<html><body>"
    output += " <h2> This page was submitted from : </h2>"  + landingpagecontent
    output += " <h2> Okay, how about this: </h2>"
    output += "<h1> %s </h1>" % messagecontent
    output += '''<form method='POST' enctype='multipart/form-data' action='/happy123'><h2>What would you like me to say?</h2><input name="message" type="text" >'''
    output += '''<input name=\"landingpage\" type=\"hidden\" value=\"happy123\">'''
    output += '''<input type="submit" value="Submit"> </form>'''
    output += "</body></html>"
    return output

  output = ""
  output += "<html>"
  output += "<body>"
  output += "<h1>Hello Happy123!</h1>"
  output += "<form method='POST' enctype='multipart/form-data' action='/happy123'>"
  output += "<h2>What would you like me to say?</h2>"
  output += "<input name=\"message\" type=\"text\" >"
  output += "<input name=\"landingpage\" type=\"hidden\" value=\"happy123\">"
  output += "<input type=\"submit\" value=\"Submit\">"
  output += "</form>"
  output += "</body>"
  output += "</html>" 
  return output

@app.route('/gloomy321', methods=['GET', 'POST'])
def showGloomy321():
  if request.method == 'POST':
    dictval = request.form.to_dict()
    print dictval
    messagecontent = dictval['message']
    landingpagecontent = dictval['landingpage']
    write_file(messagecontent, landingpagecontent)
    
    output = ""
    output += "<html><body>"
    output += " <h2> This page was submitted from : </h2>"  + landingpagecontent
    output += " <h2> Okay, how about this: </h2>"
    output += "<h1> %s </h1>" % messagecontent
    output += '''<form method='POST' enctype='multipart/form-data' action='/happy123'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
    output += "</body></html>"
    return output

  output = ""
  output += "<html>"
  output += "<body>"
  output += "<h1>Hello Gloomy123!</h1>"
  output += "<form method='POST' enctype='multipart/form-data' action='/gloomy321'>"
  output += "<h2>What would you like me to say?</h2>"
  output += "<input name=\"message\" type=\"text\" >"
  output += "<input name=\"landingpage\" type=\"hidden\" value=\"gloomy321\">"
  output += "<input type=\"submit\" value=\"Submit\">"
  output += "</form>"
  output += "</body>"
  output += "</html>" 
  return output

@app.route('/robobook', methods=['GET'])
def showRoboBook():
  output = ""
  output = read_file()
  return output

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
    output = ""
    output += "<html>"
    output += "<head>"
    output += "<style>"
    output += "table, th, td {"
    output += "border: 1px solid black;"
    output += "}"
    output += "</style>"
    output += "</head>"
    output += "<body>"
    output += "<h1>User submitted messages!</h1>"
    output += "<table>"
    for line in lines:
        data = line.split(",") 
        output += "<tr>"
        output += "<td>"
        output += data[0].strip()
        output += "</td>"

        output += "<td>"
        output += data[1].strip()
        output += "</td>"
        output += "</tr>"
    output += "</table>"
    output += "</body>"
    output += "</html>"
    print "this is the file"
    print output
    fh.close()
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
