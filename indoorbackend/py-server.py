# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import tag_solver 
from urllib.parse import urlparse
from urllib.parse import parse_qs
import numpy as np
import re
import read
import threading
from socketserver import ThreadingMixIn


#hostName = "localhost"
serverPort = 8080


def parse_anchor(line_str):
    m = re.split(";",line_str)
    if(m):
        anchor = np.zeros((len(m),2))
        for i in range(len(m)):
            n = re.split(",",m[i])
        #print(n)
            anchor[i,0] = float(n[0])
            anchor[i,1] = float(n[1])

        return anchor#[m.group(1),m.group(2)]
    else:
        return None

def parse_tdoa(line_str):
    m = re.split(";",line_str)
    if(m):
        anchor = np.zeros((len(m),len(re.split(",",m[0]))))
        for i in range(len(m)):
            n = re.split(",",m[i])
            for j in range(len(n)):
                anchor[i,j] = float(n[j])

        return anchor#[m.group(1),m.group(2)]
    else:
        return None

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            #print(self.path)
            parsed_url = urlparse(self.path)
            #print('parameter: ',parse_qs(parsed_url.query)['line'][0])
            #print('material: ',parse_qs(parsed_url.params)['line'][0])
            if parse_qs(parsed_url.query)['line'] :
                #print('line exists')
                if parse_qs(parsed_url.query)['line'][0]:
                    #print("parameter exists")
                    if parse_qs(parsed_url.query)['line'][0] != '':
                        #print('parameter is not empty string')
                        line = parse_qs(parsed_url.query)['line'][0]
                        #print('line: ',line)
                        # read.NSDI_read_TDoA_new()
                        # DDoA = parse_qs(parsed_url.query)['DDoA'][0]
                        # parsed_ddoa = parse_tdoa(DDoA)
                        # print('parsed DDoA printed here:',parsed_ddoa)
                        # anchor_location = parse_qs(parsed_url.query)['anchor_location'][0]
                        # parsed_anchor = parse_anchor(anchor_location)
                        # print('parsed anchor_location printed here:',parsed_anchor)
                        # estimation = parsed_anchor[0]
                        # args = [parsed_ddoa,parsed_anchor]
                        
                        # tag_location = tag_solver.tag_solver(estimation,args)
                        # print('tag_location',tag_location)
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()

                        #self.wfile.write(bytes("<body>", "utf-8"))

                        #self.wfile.write(bytes("<p>lines %s</p>" %line, "utf-8"))
                        self.wfile.write(bytes(line, "utf-8"))
                        #self.wfile.write(bytes("</body></html>", "utf-8"))


                        # r = requests.get("http://www.google.com")
                        # print(r.content)
                        # json_tag = json.dumps(tag_location)
            else:
                print('line does not exist')
        except:
            print('error occured')


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == "__main__":        
    #webServer = HTTPServer((hostName, serverPort), MyServer)

    # firstURL = "http://10.20.4.176:8080/page?line=hehe"
    # parsed_url = urlparse(firstURL)
    # print('parsed_url: ',parsed_url)
    # print(parse_qs(parsed_url.query)['line'][0])

    webServer = HTTPServer(('', serverPort), MyServer)
    #print("Server started http://%s:%s" % (hostname, serverPort))
    print("Server started http://%s:%s" % ('', serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")