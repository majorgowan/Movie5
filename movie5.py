from flask import Flask, request, session, render_template, url_for, json
import numpy as np
import Recommend.recommend as rec

app = Flask(__name__)
app.secret_key = 'burnsmonkeystypedit'

collaborative_mat = rec.getCosineSimilarityMatrix('cosine_coll2.npy', method='rank_sigmoid')
content_mat = rec.getCosineSimilarityMatrix('cosine_content.npy', method='rank_sigmoid')


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

    ratings_x = rec.apply_model(choices, content_mat)
    ratings_y = rec.apply_model(choices, collaborative_mat)
    ratings = zip(ratings_x,ratings_y)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
