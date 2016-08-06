from flask import Flask, request, session, render_template, url_for, json
import numpy as np

app = Flask(__name__)
app.secret_key = 'burnsmonkeystypedit'

#---ROUTES----
@app.route("/")
def movie_rater():
    session['user_choices'] = [0,0,0,0]
    return render_template('plain.html')

@app.route("/update_choice")
def update():
    # get current user choices
    choices = session['user_choices']

    # process request data to set user_choices
    poster = request.args.get('poster')
    ifilm = int(poster.split('_')[1])
    endzone = request.args.get('endzone')
    if (endzone == 'dislike_bar'):
        thumb = -1
    else:
        thumb = 1

    # set user_choices
    choices[ifilm] = thumb
    session['user_choices'] = choices

    ratings = collaborative_model(choices)

    # build response object
    resp = {}
    for ii, rating in enumerate(ratings):
        if (choices[ii] == 0):
            resp['poster_' + str(ii)] = rating  

    #pred = collaborative_model(user_choices);
    #resp = { 'ifilm': ifilm, 'thumb': thumb }

    return json.dumps(resp)

@app.route("/get_movie_list",methods=["GET"])
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
def collaborative_model(user_choices):
    fac = 1.0 / np.sum(np.abs(user_choices))
    cosine_similarity = np.array([[1, 0.9, 0.5, -0.4],
                                 [0.9, 1, -0.1, 0.6],
                                 [0.5, -0.1, 1, -0.7],
                                 [-0.4, 0.6, -0.7, 1]])
    return list(fac*cosine_similarity.dot(user_choices))
#-------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0')
