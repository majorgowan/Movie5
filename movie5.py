from flask import Flask, render_template, url_for, json
import numpy as np

app = Flask(__name__)

#---ROUTES----
@app.route("/")
def movie_rater():
    return render_template('plain.html')

@app.route("/update_choice",methods=["POST"])
def update():
    #data = request.get_json()
    '''
    ifilm = int(data['poster'].split('_')[1])
    if (data['endzone'] == 'dislike_bar'):
        thumb = 'down'
    else:
        thumb = 'up'
        
    #pred = collaborative_model(user_choices);
    resp = { 'ifilm': ifilm, 'thumb': thumb }
    '''
    resp = { 'data': "no thanks we're British" , 'isit': 'no'}
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
def collaborative_model(user_choices):
    cosine_similarity = np.array([[1, 0.9, 0.5, -0.4],
                                 [0.9, 1, -0.1, 0.6],
                                 [0.5, -0.1, 1, -0.7],
                                 [-0.4, 0.6, -0.7, 1]])
    return list(cosine_similarity.dot(user_choices))
#-------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0')
