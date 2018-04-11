
import glob

from rdflib import *

import libxmp

wav_file=glob.glob('./Musique/*/*.wav')

GlobalG= Graph()

#parcourir le dossier musique
for file in wav_file:
	# on recupere le nom du fichier
     nom=file.split('/',4)[3]
     name=nom.split('.',1)[0]
	#on stock le fichier dans un dossier
     fichier = open("./RDF/"+name+".rdf", "w")
	# lecture du chaque fichier wav
     xmpfile = libxmp.XMPFiles( file_path=file , open_forupdate=False)
	# recuperer les metadonees de chaque fichier
     xmp = xmpfile.get_xmp()

     xmpfile.close_file()

     meta = str(xmp)
     #La balise ouvrante RDF
     baliseO = meta.find('<rdf:RDF')
     #La balise fermante  RDF
     baliseF = meta.find('</rdf:RDF>')
     #...incluse
     baliseF = baliseF+len('</rdf:RDF>')
     #Calcul de la nouvelle chaine
     RDF = meta[baliseO:baliseF]
     #L'insertion des donnees dans le fichier "nomfichierWav.rdf"
     fichier.write(RDF)
     #Fermeture du fichier
     fichier.close()
     #Ajout du code RDF dans le graphe global
     GlobalG.parse("./RDF/"+name+".rdf")


#Exportation du graphe dans un fichier
GlobalG.serialize(destination='GlobalG.rdf', format='application/rdf+xml')
