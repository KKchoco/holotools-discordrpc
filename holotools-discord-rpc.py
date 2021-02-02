import discord_rpc
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import logging
import json 
from urllib.parse import urlparse
import urllib.request, json 

global parsedurl
global names
global firstconn

firstconn = 1
breaker = False

if __name__ == '__main__':
    def readyCallback(current_user):
        print('Our user: {}'.format(current_user))
        
    def disconnectedCallback(codeno, codemsg):
        print('Disconnected from Discord rich presence RPC. Code {}: {}'.format(
            codeno, codemsg
        ))

    def errorCallback(errno, errmsg):
        print('An error occurred! Error {}: {}'.format(
            errno, errmsg
        ))
        
    # Note: 'event_name': callback
    callbacks = {
        'ready': readyCallback,
        'disconnected': disconnectedCallback,
        'error': errorCallback,
    }
    

    
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        discord_rpc.initialize('386747342080049168', callbacks=callbacks, log=False)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("Body:\n%s\n", post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        parsedurl = urlparse(json.loads(post_data.decode('utf-8'))['url'], allow_fragments=False)
        if parsedurl.netloc == 'hololive.jetri.co' and parsedurl.query != "":
            with urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet&fields=items(snippet(channelTitle,channelId))&id=" + parsedurl.query.split('=')[1] + "&key=yourgoogleapikey") as url:
                data = json.loads(url.read().decode())
                global firstconn
                names = []
                if len(data['items']) != 0:
                    for x in range(len(data['items'])):    
                        with open('list.json') as f:
                            name = json.load(f)
                            def doname():
                                i = 0
                                while i <= len(name) + 1:
                                    if i == len(name):
                                        return 404
                                    if name[i]['channel_id'] == data['items'][x]['snippet']['channelId']:
                                        names.append(name[i]['channel_name'])
                                        return 0
                                    i += 1
                            if doname() == 404:
                                names.append(data['items'][x]['snippet']['channelTitle'])
                        stream = ' stream' if len(data['items']) == 1 else ' streams'
                    if len(names) < 3:
                        namess = " and ".join(names[: + len(names)])
                    else: 
                        namess = ", ".join(names[: + len(names)-2]) + ", " + " and ".join(names[-2:])
                    if firstconn == 1:
                        for a in range(0,3):
                            discord_rpc.update_presence(
                                **{
                                    'details': "Watching " + namess + stream,
                                    'start_timestamp': time.time()
                                }
                            )
                    
                            discord_rpc.update_connection()
                            time.sleep(2)
                            discord_rpc.run_callbacks()
                            firstconn = 0
                    else:
                        discord_rpc.update_presence(
                            **{
                                'details': "Watching " + namess + stream,
                                'start_timestamp': time.time()
                            }
                        )
                    
                        discord_rpc.update_connection()
                        time.sleep(2)
                        discord_rpc.run_callbacks()
                del names
        else:
            firstconn = 1
            discord_rpc.shutdown()
                    
    def log_message(self, format, *args):
        return
        
def run(server_class=HTTPServer, handler_class=S, port=6553):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
