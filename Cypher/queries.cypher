// Gráfico todos los nodos y conexiones
MATCH (node) RETURN node;

// Tabla top 10 retweets
MATCH (:Tweet)-[:RETWEETS]->(t:Tweet)
WITH t, COUNT(*) AS Retweets
ORDER BY Retweets DESC
LIMIT 10
MATCH (u:User)-[:POSTS]->(t)
RETURN u.screen_name AS User, t.text AS Tweet, Retweets;

// Dos usuarios con determinado screen_name
MATCH (n1:User), (n2:User)
WHERE n1.screen_name = "Aguada_oficial" AND n2.screen_name = "Hebraicaymacabi"
RETURN n1,n2

// TESTS

// Relaciones entre Usuarios-Tweets(para tweets que mencionan a dos usuarios)
MATCH p=(:Tweet)-[r:MENTIONS]->(n:User)
WHERE n.screen_name = "Aguada_oficial" OR n.screen_name = "Hebraicaymacabi"
RETURN p

// Todos los Usuarios que Postearon
MATCH p=(:User)-[r:POSTS]->(:Tweet)
RETURN p

// Todos los Usuarios que Retweetearon
MATCH p=(:User)-[r:RETWEETS]->(:Tweet)
RETURN p

// Usuario postea tweets
MATCH p=(:User)-[r:POSTS]->(:Tweet)
RETURN p
LIMIT 5


// Posts, retweets, replys to and mentions
MATCH usPostw=(:User)-[r:POSTS]->(:Tweet)
MATCH twRettw=(:Tweet)-[r2:RETWEETS]->(:Tweet)
MATCH twReptw=(:Tweet)-[r3:REPLY_TO]->(:Tweet)
MATCH twMenus=(:Tweet)-[r4:MENTIONS]->(:User)
RETURN usPostw,twRettw,twReptw,twMenus
LIMIT 500

MATCH a=()-[r:POSTS, r2:RETWEETS]-()
RETURN a
MATCH ()-[r2:RETWEETS]-() 
MATCH ()-[r3:REPLY_TO]-()
MATCH ()-[r4:MENTIONS]-()


// Top 10 frecuencia de Hashtags
MATCH (:Hashtag)-[:TAGS]->(:Tweet)<-[:TAGS]-(h:Hashtag)
RETURN h.name AS Hashtag, COUNT(*) AS Count
ORDER BY Count DESC
LIMIT 10

// Top 5 Tweets más retweeteado, y quien lo posteó
MATCH (:Tweet)-[:RETWEETS]->(t:Tweet)
WITH t, COUNT(*) AS Retweets
ORDER BY Retweets DESC
LIMIT 5
MATCH (u:User)-[:POSTS]->(t)
RETURN u.screen_name AS User, t.text AS Tweet, Retweets

// Todos los nodos con fechas de creación
MATCH (n)
WHERE EXISTS(n.created_at)
RETURN DISTINCT "node" as element, n.created_at AS created_at
LIMIT 25
UNION ALL MATCH ()-[r]-()
WHERE EXISTS(r.created_at)
RETURN DISTINCT "relationship" AS element, r.created_at AS created_at
LIMIT 25
