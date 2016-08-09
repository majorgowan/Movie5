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

def getCosineSimilarityMatrix(filename):
    '''retrieve cosine similarity matrix from numpy binary file
    '''
    import numpy as np
    import os.path
    return np.load(os.path.join('CosineData',filename))

def title_to_filename(title):
    '''Convert film title to filename of poster image
    '''
    import re
    return re.sub(r'[\:\-\(\)]','', \
           re.sub(r'[\.\,\s]', '_', \
           title)) + '.jpg'

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
