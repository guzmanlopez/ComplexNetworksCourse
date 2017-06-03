// Gráfico todos los nodos y conexiones
MATCH (n) RETURN n;

// Tabla top 10 retweets
MATCH (:Tweet)-[:RETWEETS]->(t:Tweet)
WITH t, COUNT(*) AS Retweets
ORDER BY Retweets DESC
LIMIT 10
MATCH (u:User)-[:POSTS]->(t)
RETURN u.screen_name AS User, t.text AS Tweet, Retweets;
