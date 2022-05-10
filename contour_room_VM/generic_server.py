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
import solver
import generic_solver


#hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            if parse_qs(parsed_url.query)['line'] :
                if parse_qs(parsed_url.query)['line'][0]:
                    if parse_qs(parsed_url.query)['line'][0] != '':
                        #if parse_qs(parsed_url.query)['line'][0] != '' and len(parse_qs(parsed_url.query)['line'][0]) > 50:
                        line = parse_qs(parsed_url.query)['line'][0]
                        line = line.replace('\x00','') #remove all the NUL characters
                        line = line[:-1]#remove the last ";"
                        print("line: ",line)
                        tagLoc = generic_solver.NSDI_read_TDoA_new(line)
                        print('tagLoc: ',tagLoc)
                        # print("tagLoc: ",tagLoc)
                        if len(tagLoc) == 2:
                            # return tagLoc
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(bytes("["+str(int(tagLoc[0]))+","+str(int(tagLoc[1]))+"]", "utf-8"))
                        else:
                            # return " "
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(bytes("", "utf-8"))
            else:
                print('line does not exist')
        except:
            print('error occured')


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == "__main__":        

    webServer = HTTPServer(('', serverPort), MyServer)
    print("Server started http://%s:%s" % ('', serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")