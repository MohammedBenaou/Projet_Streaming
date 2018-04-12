#-*- coding: utf-8 -*-

import socket, sys
import pyaudio
import wave
import cPickle

HOST = '127.0.0.1'
PORT = 7890

if (len(sys.argv) < 2):
    print("Not enough arguments! \n *** Usage: {0} <hostname> <URL>***\n".format(sys.argv[0]))
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
msgClient = sys.argv[1]


p = pyaudio.PyAudio()
print(p)

#Ouverture fichier pour enregistrement
result = wave.open('Newfile.wav', 'wb')


#Réception des paramètres du fichier audio
recept = False

while recept == False:
    sampwidth = cPickle.loads(mySocket.recv(1024))
    if not sampwidth:
        break
    recept = True
#L'envoi de ce message permet la synchronisation du client et du serveur
mySocket.send('reception') 
recept = False

while recept == False:
    nbchannels = cPickle.loads(mySocket.recv(1024))
    if not nbchannels:
        break
    recept = True
mySocket.send('reception') 
recept = False
    
while recept == False:
    framerate = cPickle.loads(mySocket.recv(1024))
    if not framerate:
        break
    recept = True

mySocket.send('reception') 
par = False
while par==False:
    params = mySocket.recv(1024)
    if not params:
        break
    result.setparams(cPickle.loads(params))
    par = True

#Ouverture du stream
stream = p.open(format=p.get_format_from_width(sampwidth),
                channels=nbchannels,
                rate=framerate,
                output=True)

#Enregistrement et diffusion du fichier reçu paquet par paquet
while 1:
    msgServeur = mySocket.recv(1024)
    if not msgServeur:
        break
    result.writeframes(msgServeur)
    stream.write(msgServeur)

#Fermeture des flux
stream.stop_stream()
stream.close()
p.terminate()
result.close()

# 4) Closing connexion :
print("\n Connexion closed.")
mySocket.close()


        
        

