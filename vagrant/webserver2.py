from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, cgitb 
import sys
from urlparse import urlparse

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello!</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/world"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello World!</body></html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/message"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html>"
            message += "<body>"
            message += "<h1>Hello!</h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            message += "<h2>What would you like me to say?</h2>"
            message += "<input name=\"message\" type=\"text\" >"
            message += "<input type=\"submit\" value=\"Submit\">"
            message += "</form>"
            message += "</body>"
            message += "</html>" 
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/message2"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html>"
            message += "<body>"
            message += "<h1>What is your message</h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            message += "<h2>What would you like me to say?</h2>"
            message += "<input name=\"message\" type=\"text\" >"
            message += "<input type=\"submit\" value=\"Submit\">"
            message += "</form>"
            message += "</body>"
            message += "</html>"
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/happy123"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html>"
            message += "<body>"
            message += "<h1>Hello Happy123!</h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            message += "<h2>What would you like me to say?</h2>"
            message += "<input name=\"message\" type=\"text\" >"
            message += "<input name=\"landingpage\" type=\"hidden\" value=\"happy123\">"
            message += "<input type=\"submit\" value=\"Submit\">"
            message += "</form>"
            message += "</body>"
            message += "</html>" 
            self.wfile.write(message)
            print message
            return 
        elif self.path.endswith("/gloomy321"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html>"
            message += "<body>"
            message += "<h1>Hello Gloomy123!</h1>"
            message += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
            message += "<h2>What would you like me to say?</h2>"
            message += "<input name=\"message\" type=\"text\" >"
            message += "<input name=\"landingpage\" type=\"hidden\" value=\"gloomy321\">"
            message += "<input type=\"submit\" value=\"Submit\">"
            message += "</form>"
            message += "</body>"
            message += "</html>" 
            self.wfile.write(message)
            print message
            return
        elif self.path.endswith("/robobook"):
         try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = read_file()
            self.wfile.write(output)
         except Exception as e:
            print e
            #print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Unexpected error:", sys.exc_info()[0]
            self.send_error(500, 'What is up: %s' % self.path)
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith("/hello"):
         try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print "\n\n\nheader is " + self.headers.getheader('content-type')            
            print "Content-type headers are"
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                print 'received multipart form-data'
                fields = cgi.parse_multipart(self.rfile, pdict)
                o = urlparse('http://www.cwi.nl:80/%7Eguido/Python.html')
                p = urlparse(self.path)
                print p
                print o
                messagecontent = fields.get('message')
                landingpagecontent = fields.get('landingpage')
                print "landing page is "  + landingpagecontent[0]
                output = ""
                output += "<html><body>"
                output += " <h2> This page was submitted from : </h2>"  + landingpagecontent[0]
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                write_file(messagecontent[0], landingpagecontent[0])
         except Exception as e:
            print e
            #print "I/O error({0}): {1}".format(e.errno, e.strerror)
            print "Unexpected error:", sys.exc_info()[0]
            self.send_error(500, 'What is up: %s' % self.path)
        
            
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


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
