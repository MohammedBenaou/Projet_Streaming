#-*- coding: utf-8 -*-

import socket, sys
import wave
import cPickle

HOST, PORT = '127.0.0.1', 7890
WEBROOT =  "./webroot" # the web server's root directory
CHUNK = 1024

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    listen_socket.bind((HOST, PORT))
except socket.error:
    print("Socket binding to given adress has failed.")
    sys.exit

listen_socket.listen(1)


print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = sys.argv[1]

    print ("Lecture du fichier : " + str(request))
    
    #Permet d'extraire le nom du fichier de la requête client
    # audio/Ambiances/neigeQuiTombe.wav
    # ../streamingapp/static/audio/Ambiances/neigeQuiTombe.wav
   # ptr = request[::-1]
    #print("Valeur ptr1: "+ str(ptr))
    #ptr = ptr[ptr.find("vaw."):ptr.find("/")]
    #print("Valeur ptr2: "+ str(ptr))
    #ptr = ptr[::-1]
    #print("Valeur ptr3: "+ str(ptr))"""
    #Ouverture du fichier wav
    wf = wave.open(request, 'rb')
    
    #Extraction des différents paramètres et envoi de ces derniers au client
    sampwidth = wf.getsampwidth()
    client_connection.sendall(cPickle.dumps(sampwidth))
    
    #La réception du message 'reception' permet la synchronisation du client et du serveur
    while client_connection.recv(1024) != 'reception':
            break        
    nchannels = wf.getnchannels()
    client_connection.sendall(cPickle.dumps(nchannels))
    while client_connection.recv(1024) != 'reception':
            break 
    framerate = wf.getframerate()
    client_connection.sendall(cPickle.dumps(framerate))
    
    while client_connection.recv(1024) != 'reception':
            break
    params = wf.getparams()
    client_connection.sendall(cPickle.dumps(params))
    
    #Récupération d'un paquet
    data = wf.readframes(CHUNK)
    
    #Envoi des paquets au client
    while data != '':
        client_connection.sendall(data)
        data = wf.readframes(CHUNK)
    
    
    #Fermeture de la connection  
    client_connection.close()
    ch = raw_input("<S>tart again <F>inish ? ")
    if ch.upper() =='F':
        break
        
