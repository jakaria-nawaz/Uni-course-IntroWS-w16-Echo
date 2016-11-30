#!/usr/bin/python

import socket
import signal
import time

class Server:
 """ Class describing a simple HTTP server objects."""

 def __init__(self, port = 80):
     """ Constructor """
     self.host = ''   # <-- works on all avaivable network interfaces
     self.port = port
     self.www_dir = 'www' # Directory where webpage files are stored

 def activate_server(self):
     """ Attempts to aquire the socket and launch the server """
     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

     try: # user provided in the __init__() port may be unavaivable
         print("Launching HTTP server on ", self.host, ":",self.port)
         self.socket.bind((self.host, self.port))

     except Exception as e:
         print ("Warning: Could not aquite port:",self.port,"\n")
         print ("I will try a higher port")
         # store to user provideed port locally for later (in case 8080 fails)
         user_port = self.port
         self.port = 8080

         try:
             print("Launching HTTP server on ", self.host, ":",self.port)
             self.socket.bind((self.host, self.port))

         except Exception as e:
             print("ERROR: Failed to acquire sockets for ports ", user_port, " and 8080. ")
             print("Try running the Server in a privileged user mode.")
             self.shutdown()
             import sys
             sys.exit(1)

     print ("Server successfully acquired the socket with port:", self.port)

     self._wait_for_connections()

 def shutdown(self):
     """ Shut down the server """
     try:
         print("Shutting down the server")
         s.socket.shutdown(socket.SHUT_RDWR)

     except Exception as e:
         print("Warning: could not shut down the socket. Maybe it was already closed?",e)

 def _gen_headers(self,  code):
     """ Generates HTTP response Headers. Ommits the first line! """

     # determine response code
     h = ''
     if (code == 200):
        h = 'HTTP/1.1 200 OK\n'
     elif(code == 404):
        h = 'HTTP/1.1 404 Not Found\n'

     # write further headers
     current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
     h += 'Date: ' + current_date +'\n'
     h += 'Server: Simple-Python-HTTP-Server\n'
     h += 'Connection: close\n\n'

     return h

 def _wait_for_connections(self):
     """ Main loop awaiting connections """
     while True:
         print ("Awaiting New connection")
         self.socket.listen(10)

         conn, addr = self.socket.accept()


         print("Got connection from:", addr)


         data = conn.recv(1024)
         string = bytes.decode(data)



         #determine request method  (HEAD and GET are supported)
         request_method = string.split(' ')[0]


        #Checking request

         x= string.find("jscall")
         if (x!=-1):
                userData=input("Type your message : ")
                conn.sendall(str.encode(userData))
                # socket only send the data to client after closing the connection.
                conn.close()

                self.activate_server()
                _wait_for_connections(self)

    
         if (request_method == 'GET') | (request_method == 'HEAD'):


             # split on space "GET /file.html" -into-> ('GET','file.html',...)
             file_requested = string.split(' ')
             file_requested = file_requested[1]

             #Check for URL arguments. Disregard them
             file_requested = file_requested.split('?')[0]

             if (file_requested == '/'):
                 file_requested = '/index.html'

             file_requested = self.www_dir + file_requested
             print ("Serving web page [",file_requested,"]")

             ## Load file content
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):  #only read the file when GET
                     response_content = file_handler.read() # read file content
                 file_handler.close()

                 response_headers = self._gen_headers( 200)

             except Exception as e:
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)

                 if (request_method == 'GET'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"

             server_response =  response_headers.encode()
             if (request_method == 'GET'):

                 server_response =  response_content


             conn.send(server_response)


             print ("Closing connection with client")
             conn.close()

         else:
             print("Unknown HTTP request method:", request_method)

def graceful_shutdown(sig, dummy):
    """ This function shuts down the server. It's triggered
    by SIGINT signal """
    s.shutdown() #shut down the server
    import sys
    sys.exit(1)

###########################################################
# shut down on ctrl+c
signal.signal(signal.SIGINT, graceful_shutdown)

print ("Starting web server")
s = Server(80)  # construct server object
s.activate_server() # aquire the socket
