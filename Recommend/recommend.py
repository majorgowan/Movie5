
def loadFilmsDF(info_file = 'result2_movies.csv'):
    '''Load dataframe with movie info from csv file
    '''
    import pandas as pd
    import os.path
    import re
    movie_df = pd.read_csv(os.path.join('CosineData',info_file))
    #movie_df['year'] = [re.match(r'.*\((.*)\)', t).group(1) for t in movie_df.title]
    return movie_df

def getMovieList():
    '''Load dataframe and return list of dictionaries with
    movie info
    '''
    df = loadFilmsDF()
    filmList = []
    for ir, row in df.iterrows():
        filmList.append({ \
                'title': row.title,
                'filename': title_to_filename(row.title)
                })
    return filmList

def getCosineSimilarityMatrix(filename, method=None):
    '''retrieve cosine similarity matrix from numpy binary file
    '''
    import numpy as np
    import os.path
    mat = np.load(os.path.join('CosineData',filename))
    if (method is not None):
        nn = len(mat)
        # create list of off-diagonal elements
        triangle = []
        for ir, r0 in enumerate(mat[:-1]):
            triangle += list(r0[ir+1:])
        triangle = np.array(triangle)

        if (method in ('rank', 'rank_sigmoid')):
            # replace similarities with equally spaced values
            # from -1 to +1
            if method == 'rank':
                vals = np.linspace(-1.0, 1.0, len(triangle))
            elif method == 'rank_sigmoid':
                sigmoid = lambda x: 2.0/(1.0+np.exp(-x)) - 1.0
                vals = np.linspace(-5, 5, len(triangle))
                vals = np.array([sigmoid(v) for v in vals])
            newvals = [a[1] for a in sorted(zip(triangle.argsort(),vals))]

        elif (method == 'centre'):
            # subtract mean of off-diagonal elements
            meanval = np.mean(triangle)
            newvals = triangle - meanval

        # reconstruct matrix from triangle array
        count = 0
        for ii in range(nn-1):
            for jj in range(ii+1,nn):
                mat[ii,jj] = newvals[count]
                mat[jj,ii] = mat[ii,jj]
                count += 1
    return mat

def title_to_filename(title):
    '''Convert film title to filename of poster image
    '''
    import re
    return re.sub(r'[\:\-\(\)]','', \
           re.sub(r'[\.\,\s]', '_', \
           title)) + '.jpg'

def apply_model(user_choices, mat, standard=False):
    '''Apply cosine-similarity matrix to user choices vector
    '''
    import numpy as np
    fac = 1.0 / np.sum(np.abs(user_choices))
    raw = mat.dot(user_choices)
    # standardize
    if standard:
        std = np.std(raw)
        ratings = [max(-0.95, min(0.95, x/std)) for x in raw] 
    else:
        ratings = [x/fac for x in raw]
    return ratings

#------------------- image prep (not for active server use -----------
def processImages(df, targetPath='static/images/posters'):
    '''Loop through dataframe df, download and save poster images as jpg
    '''
    for ir, row in df.iterrows():
        print(getSaveImage(row['url'],row['title'],targetPath))

def getSaveImage(url, title, target_path = '.'):
    '''Fetch poster image from url and save as jpg
    '''
    from PIL import Image
    import requests
    import os.path
    from io import BytesIO

    response = requests.get(url)
    # load image and resize to (?x100)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((100,100))

    # create filename
    filename = title_to_filename(title)

    img.save(os.path.join(target_path,filename))

    return filename
