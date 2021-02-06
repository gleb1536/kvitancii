# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def answer_fail(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head></head><body>FAIL! 404 <body></html>", "utf-8"))

    def answer_str(self,string):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head></head><body>%s<body></html>" % string, "utf-8"))

    def answer_kvitancia(self,uch,fio,tel,summ):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print(fio)
        self.wfile.write(bytes("<html><head></head><body>%d<br>%s<br>%s<br>%s<body></html>" % (uch,fio,tel,summ), "utf-8"))
    
    def do_GET(self):        
        url = self.path.split('?')
        real_url = url[0]
        if( len(url) > 1):
            param = url[1]
        else:
            param = ''
        if( real_url == '/summa' ):
            param = param.split('&')[0]
            id_uch= param.split('=')
            if( ( len(id_uch) > 1 ) & ( id_uch[0] == 'uch' )):
                try:
                    id_uch = int(id_uch[1])
                except:
                    self.answer_fail()
                    return
            else:
                self.answer_fail()
                return
            self.answer_str(id_uch)
            return
        elif( real_url == '/kvitancia' ):
            param = param.split('&')
            try:
                uch = param[0].split('=')
                if uch[0] == 'uch':
                    uch = int(uch[1])
                else:
                    self.answer_fail()
                    return
                FIO = param[1].split('=')
                if FIO[0] == 'fio':
                    FIO = FIO[1]
                else:
                    self.answer_fail()
                    return
                tel = param[2].split('=')
                if tel[0] == 'tel':
                    tel = tel[1]
                else:
                    self.answer_fail()
                    return
                summ = param[3].split('=')
                if summ[0] == 'summ':
                    summ = summ[1]
                else:
                    self.answer_fail()
                    return
                self.answer_kvitancia(uch,FIO,tel,summ)
            except:
                self.answer_fail()
                return
        else:
            self.answer_fail()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
