from flask import Flask, request, session, render_template, url_for, json
import numpy as np
import Recommend.recommend as rec

app = Flask(__name__)
app.secret_key = 'burnsmonkeystypedit'

collaborative_mat = rec.getCosineSimilarityMatrix('cosine_coll2.npy', method='centre')
content_mat = rec.getCosineSimilarityMatrix('cosine_content.npy', method='centre')

#---ROUTES----
@app.route("/")
def movie_rater():
    session['user_choices'] = list(np.zeros(len(content_mat)))
    # initialize random y-coordinate:
    session['ratings_y'] = list(2.0*np.random.sample(len(content_mat)) - 1.0)
    return render_template('plain.html')

@app.route("/update_choice")
def update():
    # get current user choices
    choices = session['user_choices']

    # process request data to set user_choices
    poster = request.args.get('poster')
    print(poster)

    # if request isn't just a radio change
    if poster != 'radio':
        ifilm = int(poster.split('_')[1])
        endzone = request.args.get('endzone')
        if (endzone == 'dislike_bar'):
            thumb = -1.0
        else:
            thumb = 1.0
        choices[ifilm] = thumb
        # set user_choices (in case of change)
        session['user_choices'] = choices

    filter_method = request.args.get('filter_method')
    if (filter_method == 'content'):
        ratings_x = rec.apply_model(choices, content_mat, standard=True)
    else:
        ratings_x = rec.apply_model(choices, collaborative_mat, standard=True)

    ratings = zip(ratings_x,session['ratings_y'])

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
