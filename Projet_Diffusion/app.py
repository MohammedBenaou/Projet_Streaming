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
    print(gender)
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
           ?a xmpDM:artist ?artistName .
           }""")

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


    return render_template('index.html',
                           gender=gender,
                           listeChansons=listeChansons,
                           artist=artist,
                           composer=composer,
                           subject=subject,
                           rating=rating)


if __name__ == '__main__':
    app.run(debug=True)
