# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import urllib
import forming

hostName = "0.0.0.0"
serverPort = 80
form = 0

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
        self.wfile.write(bytes(str(string), "utf-8"))

    def answer_form(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = open("form.html", 'rb').read()
        self.wfile.write(content)

    def answer_file(self,filename):
        self.send_response(200)
        self.send_header("Content-type", "ya-river.pdf")
        self.end_headers()
        content = open(filename, 'rb').read()
        self.wfile.write(content)

    def answer_kvitancia(self,uch,fio,tel1,tel2,summ):
        fio = fio.encode('utf8')
        print(fio)
        file_n = form.form(uch,fio,tel1,tel2,summ,self.client_address[0])
        self.answer_file(file_n)
                
    
    def do_GET(self):  
        url =  urllib.parse.unquote(self.path)  
        url = url.split('?')
        real_url = url[0]
        print(self.client_address)
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
                    if ( ( id_uch > 0 ) & ( id_uch < 530 ) ):
                        self.answer_str(form.summa[id_uch])
                        return
                except:
                    self.answer_fail()
                    return
            else:
                self.answer_fail()
                return
            self.answer_fail()
            return
        elif( real_url == '/kvitancia' ):
            param = param.split('&')
            
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
            tel1 = param[2].split('=')
            if tel1[0] == 'tel1':
                tel1 = tel1[1]
            else:
                self.answer_fail()
                return
            tel2 = param[3].split('=')
            if tel2[0] == 'tel2':
                tel2 = tel2[1]
            else:
                self.answer_fail()
                return
            summ = param[4].split('=')
            if summ[0] == 'summ':
                summ = summ[1]
            else:
                self.answer_fail()
                return
            self.answer_kvitancia(uch,FIO,tel1,tel2,summ)

            try:
                pass
            except:
                self.answer_fail()
                return
        elif( real_url == '/' ):
            self.answer_form()
        else:
            self.answer_fail()

if __name__ == "__main__":
    form = forming.forming()
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
