from flask import Flask, request, session, render_template, url_for, json
import numpy as np
import Recommend.recommend as rec

app = Flask(__name__)
app.secret_key = 'burnsmonkeystypedit'

collaborative_mat = rec.getCosineSimilarityMatrix('cosine_coll2.npy')
content_mat = rec.getCosineSimilarityMatrix('cosine_content.npy')

#---ROUTES----
@app.route("/")
def movie_rater():
    session['user_choices'] = list(np.zeros(len(content_mat)))
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
        thumb = -1.0
    else:
        thumb = 1.0

    # set user_choices
    choices[ifilm] = thumb
    session['user_choices'] = choices

    ratings_x = apply_model(choices, 'content')
    ratings_y = apply_model(choices, 'collaborative')
    ratings = zip(ratings_x,ratings_y)

    # print(list(ratings))

    # build response object
    resp = {}
    for ii, rating in enumerate(ratings):
        if (choices[ii] == 0):
            resp['poster_' + str(ii)] = rating  

    return json.dumps(resp)

@app.route("/get_movie_list",methods=["GET"])
def getMovieList():
    # create dictionary of movie info and send as JSON
    resp = rec.getMovieList()
    return json.dumps(resp)

#-------------------
def apply_model(user_choices, coll_content):
    fac = 1.0 / np.sum(np.abs(user_choices))
    if coll_content == 'collaborative':
        cosine_similarity = collaborative_mat
    else:
        cosine_similarity = content_mat

    return list(fac*cosine_similarity.dot(user_choices))
#-------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0')
