"""
Twitter

@author: Guzmán
"""

import tweepy
import time
import json
#import networkx
#import numpy

# OAuthentication
with open('twitter-OAuth.py') as oauth:
    exec(oauth.read())

# Create API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# Get followers from elpaisuy
followersElPais = []

cursorElPais = tweepy.Cursor(api.followers, screen_name="elpaisuy", count=200).items()

while True:
    try:
        user = next(cursorElPais) # OK sigue
    except tweepy.TweepError:
        time.sleep(60*15) # espera 15 minutos
        user = next(cursorElPais)
    except StopIteration:
        break # sale
    #print("> user:", user.__dict__) # imprime usuarios
    with open('elPaisFollowers.json', 'a') as f:
        f.write(json.dumps(user._json)) # escribe a un archivo haciendo append
    followersElPais.append(user) # agrega usuario a la lista

# Ask length
len(followersElPais)

# Load json data
with open('elPaisFollowers.json') as json_file:
    json_data = json.loads(json_file)
    print(json_data)




# Save El Pais followers CSV
# numpy.savetxt("idsFollowersElPais.csv", followersElPais, delimiter=",")


# Which users follow both


# Which users retweet from el Pais


# Which users retweet from La Diaria



