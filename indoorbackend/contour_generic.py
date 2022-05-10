# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import numpy as np
from socketserver import ThreadingMixIn
import all_solver
import best_solver

serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            #“x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04@roomwidth*roomheight@seed_choice@dop@sigma@count;”
            parsed_url = urlparse(self.path)
            if parse_qs(parsed_url.query)['line'] :
                if parse_qs(parsed_url.query)['line'][0]:
                    if parse_qs(parsed_url.query)['line'][0] != '':
                    #if parse_qs(parsed_url.query)['line'][0] != '' and len(parse_qs(parsed_url.query)['line'][0]) > 50:
                        line = parse_qs(parsed_url.query)['line'][0]
                        line = line.replace('\x00','') #remove all the NUL characters
                        line = line[:-1]#remove the last ";"
                        # print("line: ",line)
                        parts = line.split('@')
                        dop = parts[4]
                        if dop == "all":
                            tag_candidates = all_solver.NSDI_read_TDoA_new(line)
                            print('all anchors used')
                        if dop == "best":
                            print('best anchors used')
                            tag_candidates = best_solver.NSDI_read_TDoA_new(line)
                            # print('best anchors used')
                        # print('tagLoc: ',tagLoc)
                        # print("tagLoc: ",tagLoc)
                        # print('tag_candidates shape: ',tag_candidates.shape)
                        if len(tag_candidates[0]) == 2:
                            # return tagLoc
                            # print('getshape2')
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            # print("we here")
                            # self.wfile.write(bytes("["+str(int(tagLoc[0]))+","+str(int(tagLoc[1]))+"]", "utf-8"))
                            serialized = json.dumps(tag_candidates.tolist())
                            # print("serialized: ",serialized)
                            # print('typeofserial: ',type(serialized))
                            self.wfile.write(bytes(serialized,'utf-8'))
                            print('sent')
                        else:
                            # return " "
                            # print('getshape1')
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            serialized = json.dumps([""])
                            print('serialized created')
                            self.wfile.write(bytes(serialized, "utf-8"))
                            print('sent')
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