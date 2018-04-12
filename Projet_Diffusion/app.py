#! /usr/bin/python
# -*- coding:utf-8 -*-
import rdflib

from flask import request, Flask, render_template, redirect
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    g = rdflib.Graph()

# ... add some triples to g somehow ...
    g.parse("GlobalG.rdf")

    gender = g.query(
        """SELECT DISTINCT ?genre
           WHERE {
              ?x xmpDM:genre ?genre .
              
           } ORDER BY ASC(?genre) """)
        
    qres1 = g.query(
        """SELECT DISTINCT ?x
           WHERE {
              ?x xmpDM:genre ?genre .
              
           }""")
    
    listeChansons = [""]
    for row in qres1:
        stringRow = str(row.x)
        splitRow = stringRow.split("/")
        chanson = splitRow[len(splitRow) - 1]
        music = chanson.split('.',1)[0]
        Liste=music+str(".wav")
        listeChansons.append(Liste)
        
    artist = g.query(
        """SELECT DISTINCT ?artistName
           WHERE {
              ?x xmpDM:artist ?artistName .
              
           } ORDER BY ASC(?artistName)""")
    
    composer = g.query(
        """SELECT DISTINCT ?composerName
           WHERE {
              ?a xmpDM:composer ?composerName .
              
           } ORDER BY ASC(?composerName) """)

    subject = g.query(
        """SELECT DISTINCT ?sujet
           WHERE {
              ?a dc:subject ?na . ?na ?x ?sujet . FILTER (?x != rdf:type)
              
           } ORDER BY ASC(?sujet) """)
    
    rating = g.query(
        """SELECT DISTINCT ?rating
           WHERE {
              ?a xmp:Rating ?rating 
              
           } ORDER BY ASC(?rating)""")
    return render_template('index.html',gender=gender, 
                           listeChansons=listeChansons, 
                           artist=artist, 
                           composer=composer, 
                           subject=subject, 
                           rating=rating)

@app.route('/result',methods = ['POST', 'GET'])
def result():

  result_genre= request.form['genre']
  result_rating= request.form['rank']
  result_artist= request.form['artiste']
  result_sujet= request.form['sujet']
  
  g=rdflib.Graph()
  g.parse("GlobalG.rdf")

    #query = "SELECT DISTINCT ?x WHERE { ?x <http://ns.adobe.com/xmp/1.0/DynamicMedia/artist> \"Hicham Chahidi\" . }"


  query = "SELECT DISTINCT ?x WHERE { "
    #Artiste
  if result_artist != "":
    query = query + "?x <http://ns.adobe.com/xmp/1.0/DynamicMedia/artist> \"" + result_artist + "\" . "
  else:
    query = query + "?x <http://ns.adobe.com/xmp/1.0/DynamicMedia/artist> ?artist . "

  #Rating
  if result_rating != "":
    query = query + "?x <http://ns.adobe.com/xap/1.0/Rating> \"" + result_rating + "\" . "
  query = query + "?x <http://ns.adobe.com/xap/1.0/Rating> ?rating . "

  #Genre
  if result_genre != "":
    query = query + "?x <http://ns.adobe.com/xmp/1.0/DynamicMedia/genre> \"" + result_genre + "\" . "
  else:
    query = query + "?x <http://ns.adobe.com/xmp/1.0/DynamicMedia/genre> ?genre . "

  #Titre
  query = query + "?x <http://purl.org/dc/elements/1.1/title> ?y . "
  query = query + "?y ?prop1 ?title . "

  #Sujet
  if result_sujet != "":
    query = query + "?z <http://purl.org/dc/elements/1.1/subject> \"" + result_sujet + "\" . "
  else:
    query = query + "?z ?prop2 ?subject . "

  #Filtres
  query = query + " FILTER(?prop1 != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) . "
  query = query + " FILTER(?prop2 != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>) . "
  query = query + " }"

  print (query)
  results = g.query(query)
  return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

