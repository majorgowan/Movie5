from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

#---ROUTES----
@app.route("/")
def movie_rater():
    return render_template('plain.html')

@app.route("/update_choice",methods=["POST"])
def update():
    # dumb dumb model, just send nudge distances for all movies
    resp = { 'nudge': nudge_model() }
    return json.dumps(resp)

@app.route("/get_movie_list",methods=["POST"])
def getMovieList():
    # create dictionary of movie info and send as JSON
    resp = \
       [  
       { 
           'title': 'The Bourne Identity (2002)',
           'filename': 'BourneIdentity_2002_t.jpg'
       },
       {
           'title': 'The Bourne Supremacy (2004)',
           'filename': 'BourneSupremacy_2004_t.jpg'
       },
       {
           'title': 'The Bourne Ultimatum (2007)',
           'filename': 'BourneUltimatum_2007_t.jpg'
       },
       {
           'title': 'Jason Bourne (2016)',
           'filename': 'JasonBourne_2016_t.jpg'
       },
       ]
    return json.dumps(resp)

#-------------------
def nudge_model():
    import random
    nudge = [random.randint(0,200) for i in range(4)]
    return nudge
#-------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0')
