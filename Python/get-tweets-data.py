#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 20:06:09 2017

@author: guzman
"""

# Import python libraries

import tweepy
import time
from py2neo import authenticate, Graph
from random import choice

# Twitter authentication
# OAuthentication
with open('../twitter-OAuth.py') as oauth:
    exec(oauth.read())

# Create API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

# Neo4j DB graph authentication and build some constraints

# Connect to graph
url = "http://localhost:7474/db/data/"
authenticate("localhost:7474", neo4jUser, neo4jPass)
graph = Graph(url)

# Add uniqueness constraints
graph.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (l:Link) ASSERT l.url IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (s:Source) ASSERT s.name IS UNIQUE;")

# Query words
queries = ["aguada", "aguatero", "hebraica", "macabi", "finalesLUB", "juntosporlanovena", "vamossha", "finaleslub"]

# Add query string to filename
q = ""
for qry in queries: q += "_" + qry

# Open file connection to append usernames
ufile = open("usernames{}.txt".format(q), "a")

# Parameters
count = 100
result_type = "mixed"
until = "2017-05-28"
lang = "es"
since_id = -1
place = api.geo_search(query="Uruguay", granularity="country")
place_id = place[0].id

# Add place to queries
queries.append("place:{}".format(place_id))

def search_tweets(query, since_id):
    return api.search(q=query, count=count, until=until, result_type=result_type, lang=lang, since_id=since_id)

while True:
    try:
        q = choice(queries)
        tweets = search_tweets(q, since_id)
        if tweets:
            plural = "s." if len(tweets) > 1 else "."
            print("Found " + str(len(tweets)) + " tweet" + plural)
        else:
            print("No tweets found.\n")
            time.sleep(65)
            continue

        since_id = tweets[0].id

        # Pass dict to Cypher and build query from cypher script file        
        with open('/home/guzman/Documentos/GitLab/ComplexNetworks/Cypher/queries-in-script.cypher') as query:
            query = query.read()        
        
        # Send Cypher query.
        graph.run(query, tweets=[tweet._json for tweet in tweets])

        # adding users to user list
        for tweet in tweets:
            ufile.write(tweet.user.screen_name+"\n")
        print("Tweets added to graph! \n")
        time.sleep(33)

    except Exception as e:
        print(e)
        time.sleep(33)
        continue


# Import graph to python - queries

# Return all the nodes in the DB
a = graph.run('MATCH (n) RETURN n;')








