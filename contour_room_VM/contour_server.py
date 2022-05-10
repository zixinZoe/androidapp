from http.server import CGIHTTPRequestHandler, HTTPServer
import math
from socketserver import ThreadingMixIn
import statistics
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.request
import json
# from flask import Flask

from matplotlib.cbook import report_memory

from server import MyServer
import numpy as np
import requests

serverPort = 443
class MyServer(CGIHTTPRequestHandler):

    def do_GET(self):
        try:
#"e.g. anchorLoc=1500,1500;1500,2500;2500,1500;2500,2500&roomSize=4000*4000&gradient=0;3000;100&sampleDistance=200&sigma=50&maxErrShown=10000&iniSeed=roomCenter/origin/custom&customSeed=20,20&dop=all/best&count=50"
            # print('gethere')
            # c = 299792458
            anchors = ""
            tdoalist = []
            locs = np.zeros((20,2))
            # mu, sigma = 0, 100
            respNum = 0
            xs = []
            ys = []
            sample_distance = 0
            error_matrix = []
            errlimit = 0
            sigma = 0
            count = 0
            seed = ""
            seed_choice = ""
            parsed_url = urlparse(self.path)
            # print("parsed_url: ",parsed_url)
            if parse_qs(parsed_url.query)['sampleDistance'] : # read anchor locations
                sample_distance = parse_qs(parsed_url.query)['sampleDistance'][0]
                sample_distance = int(sample_distance)
            if parse_qs(parsed_url.query)['anchorLoc'] : # read anchor locations
                anchors = parse_qs(parsed_url.query)['anchorLoc'][0]
                # print(anchors)
                read_locs = anchors.split(";")
                num = 0
                respNum = len(read_locs)
                for read_loc in read_locs: 
                    coors = read_loc.split(",")
                    x = int(coors[0])
                    y = int(coors[1])
                    locs[num][0] = x
                    locs[num][1] = y
                    num = num+1
            if parse_qs(parsed_url.query)['roomSize'] : # read room size
                room = parse_qs(parsed_url.query)['roomSize'][0]
                read_size = room.split("*")
                roomX = int(read_size[0])
                roomY = int(read_size[1])
                xs = range(0,roomX+1,sample_distance)
                # print('xs size: ',len(xs))
                xs = [ele for ele in xs for i in range(0,roomY+1,sample_distance)]
                ys = range(0,roomY+1,sample_distance)
                for x in range(0,roomX+1,sample_distance):
                    for y in range(0,roomY+1,sample_distance):
                        # print("x: ",x)
                        # print("y: ",y)
                        tdoas = ""
                        for respIdx in range(1,respNum):
                            # print("anchors: ",respIdx)
                            s1 = np.sqrt((locs[respIdx][0]-x)**2+(locs[respIdx][1]-y)**2)
                            s2 = np.sqrt((locs[0][0]-x)**2+(locs[0][1]-y)**2)
                            tdoa = s1-s2
                            # cur_tdoa = []
                            # noise = np.random.normal(mu, sigma,100)
                            # for i in range(100):
                            #     cur_tdoa.append(tdoa + noise[i])
                            tdoas= tdoas+str(tdoa)+";"
                        tdoas = tdoas[:-1]
                        tdoalist.append(tdoas)
                        # print('tdoalength: ',len(tdoalist))
            if parse_qs(parsed_url.query)['maxErrShown'] : # read room size
                errlimit = parse_qs(parsed_url.query)['maxErrShown'][0]
                errlimit = int(errlimit)
            if parse_qs(parsed_url.query)['iniSeed'] : # read room size
                seed = parse_qs(parsed_url.query)['iniSeed'][0]
                if seed == "origin":
                    seed_choice = "0,0"
                if seed == "roomCenter":
                    seed_choice = "rmctr"
                    # print('seed_choice: ',seed_choice)
                if seed == "custom":
                    if parse_qs(parsed_url.query)['customSeed'] : # read room size
                        seed_choice = parse_qs(parsed_url.query)['customSeed'][0]
            if parse_qs(parsed_url.query)['dop'] : # read room size
                dop = parse_qs(parsed_url.query)['dop'][0]
            if parse_qs(parsed_url.query)['sigma'] : # read anchor locations
                sigma = parse_qs(parsed_url.query)['sigma'][0]
            if parse_qs(parsed_url.query)['count'] : # read room size
                count = parse_qs(parsed_url.query)['count'][0]

            index = 0
            for tdoa in tdoalist:
                # for i in range(100):
                #     noise = np.random.normal(mu, sigma)
                #     tdoa = tdoa + noise
                line = anchors+"@"+tdoa+"@"+room+"@"+seed_choice+"@"+dop+"@"+sigma+"@"+count+";"
                #“x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04@roomwidth*roomheight@seed_choice@dop@sigma@count” 
                curUrl = "http://localhost:8080/path"
                # print("line: ",line)
                PARAMS = {"line":line}
                tag_candidates = json.loads(requests.get(url = curUrl,params=PARAMS).text)
                # print('deserialized: ',tag_candidates)
                errors = []
                error = None
                for tag in tag_candidates:
                    # print('tag: ',tag)
                    if tag != "":
                        x = tag[0]
                        y = tag[1]
                        error = math.sqrt((x-xs[index])**2+(y-ys[(index+1) % len(ys)-1])**2)
                        # print('error: ',error)
                        errors.append(error)
                    else:
                        # print('tag == ""')
                        errors.append(errlimit) #if no result, set error as limit
                median_error = statistics.median(errors)
                # print("median error: ",median_error)
                # print('errlimit: ',errlimit)
                if median_error <=errlimit:
                    error_matrix.append(median_error/1000)
                    index = index + 1
                else:
                    error_matrix.append(errlimit/1000)
                    index = index +1
                # print("errormatrix: ",error_matrix)
            # if len(error_matrix)<(int(roomX/200)*int(roomY/200)):
            #     error_matrix.append(0)
            # print('error_matrixgot')
            # print('error_matrixshape: ',np.array(error_matrix).shape)
            # print('x: ',int((roomX+1)//200))
            # print('y; ',int((roomY+1)//200))
            error_matrix = np.array(error_matrix).reshape((int((roomX+1)//sample_distance+1),int((roomY+1)//sample_distance)+1))
            # print('shape error_matrix: ',error_matrix.shape)
            # print('error matrix: ',error_matrix)
            self.send_response(200)
            # self.send_header("Content-type", "text/html")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            serialized = json.dumps(np.transpose(error_matrix).tolist())
            # print("serialized: ",serialized)
            # print("serialized")
            self.wfile.write(bytes(serialized,'utf-8'))
            print('sent')
            #create a GET request to generic_server.py here
        except:
            print('try failed')



# app = Flask(__name__)
# @app.route("file:///Users/yinzixin/Desktop/indoorbackend/index.html")
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