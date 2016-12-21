from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import subprocess
from datetime import datetime



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cmd = self.path[1:]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        subprocess.Popen(["python", "run.py", "-cmd="+cmd, "-log="+timestamp+'_balancing.log'])
        # Send the html message
        return self.wfile.write("Started new thread with command " + cmd)


def run_server():
    port = 8080
    handler = MyHandler
    httpd = HTTPServer(("", port), handler)
    print ("serving at port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
