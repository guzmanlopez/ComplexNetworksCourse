#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Jun  2 20:06:09 2017

@author: guzman
"""

# Import python libraries
import tweepy
import time
from random import choice
from py2neo import authenticate, Graph
import cypher
import networkx as nx

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

connPar = "http://" + neo4jUser + ":" + neo4jPass + "@localhost:7474/db/data/"

# Add uniqueness constraints
graph.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (l:Link) ASSERT l.url IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (s:Source) ASSERT s.name IS UNIQUE;")

# Query words
queries = ["aguada", "aguatero", "hebraica", "macabi", "finalesLUB", "juntosporlanovena", "vamossha", "finaleslub"]

# get Uruguay ID code
#place = api.geo_search(query="Uruguay", granularity="country")
#place_id = place[0].id
# Add place to queries
#queries = ("place:{}".format(place_id)) + " AND " + queries

# Add tags
q = "aguada-hebraica"

# Open file connection to append usernames
ufile = open("usernames_{}.txt".format(q), "a")

# Pass dict to Cypher and build query from cypher script file
with open('/home/guzman/Documentos/GitLab/ComplexNetworks/Cypher/queries-in-script.cypher') as query:
    query = query.read()

# Parameters
count = 100 # The number of tweets to return per page, up to a maximum of 100. Defaults to 15.
result_type = "mixed" # Include both popular and real time results in the response.
until = "2017-06-04" # Returns tweets created before the given date.
lang = "es" # Restricts tweets to the given language
since_id = -1 # Returns results with an ID greater than (that is, more recent than) the specified ID.

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
# https://nicolewhite.github.io/neo4j-jupyter/hello-world.html

# Return all the nodes in the DB
data = graph.run('')

data = graph.run('MATCH usPostw=(:User)-[r:POSTS]->(:Tweet) MATCH twRettw=(:Tweet)-[r2:RETWEETS]->(:Tweet) MATCH twReptw=(:Tweet)-[r3:REPLY_TO]->(:Tweet) MATCH twMenus=(:Tweet)-[r4:MENTIONS]->(:User) RETURN usPostw,twRettw,twReptw,twMenus LIMIT 10;')

data = [tuple(x) for x in data]

for d in data:
    print(d)

results = cypher.run('MATCH usPostw=(:User)-[r:POSTS]->(:Tweet) MATCH twRettw=(:Tweet)-[r2:RETWEETS]->(:Tweet) MATCH twReptw=(:Tweet)-[r3:REPLY_TO]->(:Tweet) MATCH twMenus=(:Tweet)-[r4:MENTIONS]->(:User) RETURN usPostw,twRettw,twReptw,twMenus LIMIT 100;', conn=connPar)

g = results.get_graph()
nx.draw(g)

g.nodes(data=True)

nx.info(g)

nx.degree_histogram(g)

# Degrees
deg = nx.degree(g)

# Número de nodos y ejes
numNod = nx.number_of_nodes(g)
numEdg = nx.number_of_edges(g)

# Componentes conectados
conComp = nx.number_connected_components(g)

# Componentes conexas
cns = nx.connected_components(g)

# Diámetro
d = nx.diameter(g)

# Excentricidad
ecc = nx.eccentricity(g)

# Centro
cen = nx.center(g)

# Periferia
per = nx.periphery(g)

# Transistividad
tr = nx.transitivity(g)

# Resumen
print("componentes conexas: ", cns)
print("diameter: %s" % d)
print("eccentricity: %s" % ecc)
print("center: %s" % cen)
print("periphery: %s" % per)

# 3d visualization
import jgraph

jgraph.draw(data)