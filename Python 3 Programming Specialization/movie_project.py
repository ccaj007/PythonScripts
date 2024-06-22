# https://github.com/ananyabisht07/COURSERA-Python-3-Programmming-/blob/master/COURSE_3%3AData%20Collection%20and%20Processing%20with%20Python/Week_3/Course_3(project).ipynb

import API_KEYS
import requests
import json
import pprint

def get_movies_from_tastedrive(query):
    base_url="https://tastedive.com/api/similar"
    params_diction = {}
    params_diction['q'] = query
    params_diction['type'] = 'movie'
    params_diction['limit'] = 5
    params_diction['k'] = API_KEYS.tastedrive_API

    response = requests.get(base_url, params = params_diction)
    #print(response.url)
    return response.json()

def extract_movie_titles(movie):
#    pprint.pprint(movie)
    dic = movie['similar']
    l=len(dic['results'])
    li=[]
    for i in range(l):
        li.append(dic['results'][i]['name'])    
    return li
    
def get_movie_data(movie):

r = extract_movie_titles(get_movies_from_tastedrive('black panther'))
print(r)

