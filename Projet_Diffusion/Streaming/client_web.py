#-*- coding: utf-8 -*-

import socket, sys

HOST = '127.0.0.1'
PORT = 7800

if (len(sys.argv) < 2):
    print("Not enough arguments! \n *** Usage: {0} <hostname> ***\n".format(sys.argv[0]))
    sys.exit()




# 1) creation of a socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2) try to connect to the server:
try:
    mySocket.connect((HOST, PORT))

except socket.error:
    print("Connexion has failed.")
    sys.exit()    
print("Connected to the server.")

# 3) Interacts with the server:
msgClient = "HEAD / HTTP/1.0"
#Ajout de la methode GET
#msgClient = "GET / HTTP/1.1"
msgClient = "GET /audio.ram HTTP/1.1"
#msgClient = "GET /image.jpg HTTP/1.1"
#msgClient = "GET /favi.ico HTTP/1.1"

mySocket.send(msgClient.encode("Utf8"))

while 1:
    msgServeur = mySocket.recv(1024).decode("Utf8")
    if not msgServeur:
        break
    print(msgServeur)
 
# 4) Closing connexion :
print("\n Connexion closed.")
mySocket.close()

        
        

