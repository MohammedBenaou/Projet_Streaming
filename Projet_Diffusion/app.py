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
   g = rdflib.Graph()

# ... add some triples to g somehow ...
   g.parse("GlobalG.rdf")
   if request.method == 'POST':
      result = request.form
      if(request.form['genre'] != ''):
          titles = search_by_genre(request.form['genre'])

      if(request.form['rank'] != ''):
          titles = search_by_ranking(request.form['rank'])

      if(request.form['artiste'] != ''):
          titles = search_by_artist(request.form['artiste'])

      for row in titles:
         for col in row:
            print (col)
      return render_template("index.html",titles=titles)

def search_by_artist(artist):
    g = rdflib.Graph()
    g.parse("GlobalG.rdf")
    titles = g.query(
            """PREFIX xmpDM: <http://ns.adobe.com/xmp/1.0/DynamicMedia/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    SELECT DISTINCT ?artist
    WHERE {
      ?res xmpDM:genre  """+"\"" +artist+ "\"" + """ .
      ?res dc:title ?na . ?na ?x ?titre . FILTER (?titre != rdf:Alt) 
    }
    ORDER BY(?artist)""")
    return titles

def search_by_genre(genre):
	g = rdflib.Graph()
	g.parse("GlobalG.rdf")

	titles = g.query(
            """PREFIX xmpDM: <http://ns.adobe.com/xmp/1.0/DynamicMedia/>
		PREFIX dc: <http://purl.org/dc/elements/1.1/>
		SELECT DISTINCT  ?titre
		WHERE {
			?res xmpDM:genre  """+"\"" +genre+ "\"" + """ .
			?res dc:title ?na . ?na ?x ?titre . FILTER (?titre != rdf:Alt) 
		} ORDER BY ASC(?titre)
		""")
	return titles

def search_by_ranking(rank):
	g = rdflib.Graph()
	g.parse("GlobalG.rdf")

	titles = g.query(
            """PREFIX xmp:<http://ns.adobe.com/xap/1.0/>
		PREFIX dc: <http://purl.org/dc/elements/1.1/>
		SELECT  DISTINCT ?titre
		WHERE { 
			?res  xmp:Rating  """+"\"" +rank+ "\"" + """ .
			?res dc:title ?na . ?na ?x ?titre . FILTER (?titre != rdf:Alt) 
		}ORDER BY ASC(?titre)

		""")
	return titles



if __name__ == '__main__':
    app.run(debug=True)

