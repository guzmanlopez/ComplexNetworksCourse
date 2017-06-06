# [Curso *"De las redes complejas a las redes sociales: Introducción al Uso del Big Data"*][d6115b6a]

[d6115b6a]: http://desarrolloterritorial.ei.udelar.edu.uy/?p=2618 "webpage"

## Espacio Interdisciplinario

![Afiche curso](http://desarrolloterritorial.ei.udelar.edu.uy/wp-content/uploads/2017/05/Curso-Modeling_BANNER_AFICHE.png)

---

# Trabajo final

Para cargar la base de datos de grafos hay que copiar todos los archivos de la carpeta `graphdb` a la carpeta `/var/lib/neo4j/data/databases/graph.db/ `.

```bash
sudo cp -v /graphdb/* /var/lib/neo4j/data/databases/graph.db/

```


# Análisis de la red de *tweets* y usuarios relacionados con la final de la Liga Uruguaya de Basketball (LUB).

## Trabajo final del curso "De las redes complejas a las redes sociales: Introducción al Uso del Big Data"


### Integrantes del equipo:

- Andrea Apolaro
- Guzmán López
- Leticia Vidal
- Ricardo Rezzano


## Introducción

En el marco del curso ...



## Metodología

Se utilizó el lenguaje de programación Python (versión 3.6.1) ...

Importar librerías


```python
# Import python libraries
import tweepy
import time
from random import choice
from py2neo import authenticate, Graph
import cypher
import networkx as nx
import matplotlib.pyplot as plt
```

Autenticación de Twitter y Neo4j mediante la lectura de un archivo externo con las claves requeridas:


```python
import tweepy

# Twitter OAuthentication
consumer_key = "XXXXXXXXXX"
consumer_secret = "XXXXXXXXXX"
access_token = "XXXXXXXXXX"
access_token_secret = "XXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Neo4j
neo4jUser = "xxxx"
neo4jPass = "xxxx"
```


```python
# Authentication credentials for Tweeter and Neo4j credentials
with open('/home/guzman/Documentos/Cursos/Redes Complejas - Introducción al uso del Big Data/Python/twitter-OAuth.py') as oauth:
    exec(oauth.read())
```

Crear la API (Application Program Interface) de Twitter:


```python
# Create API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
```

Comenzar el servicio de la base de datos Neo4j desde una consola:


```python
%%sh

# Start neo4j service
systemctl start neo4j.service

# Check status of neo4j service
systemctl status neo4j.service
```

    ● neo4j.service - Neo4j
       Loaded: loaded (/usr/lib/systemd/system/neo4j.service; disabled; vendor preset: disabled)
       Active: active (running) since Tue 2017-06-06 08:40:45 -03; 4ms ago
      Process: 1486 ExecStart=/usr/bin/neo4j start (code=exited, status=0/SUCCESS)
     Main PID: 1546 (java)
        Tasks: 40 (limit: 4915)
       Memory: 22.5M
          CPU: 131ms
       CGroup: /system.slice/neo4j.service
               └─1546 /usr/sbin/java -cp /usr/share/java/neo4j/plugins:/etc/neo4j:/usr/share/java/neo4j/*:/usr/share/java/neo4j/plugins/* -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow -XX:hashCode=5 -XX:+AlwaysPreTouch -XX:+UnlockExperimentalVMOptions -XX:+TrustFinalNonStaticFields -XX:+DisableExplicitGC -Djdk.tls.ephemeralDHKeySize=2048 -Dunsupported.dbms.udc.source=tarball -Dfile.encoding=UTF-8 org.neo4j.server.CommunityEntryPoint --home-dir=/usr/share/neo4j --config-dir=/etc/neo4j

    jun 06 08:40:45 carqueja systemd[1]: Starting Neo4j...
    jun 06 08:40:45 carqueja neo4j[1486]: Starting Neo4j.
    jun 06 08:40:45 carqueja neo4j[1486]: Started neo4j (pid 1546). By default, it is available at http://localhost:7474/
    jun 06 08:40:45 carqueja systemd[1]: Started Neo4j.


Autenticación de la base de datos no relacional Neo4j a través de la lectura del archivo externo con las claves de usuario y contraseña requeridas leído anteriormente.


```python
# Neo4j DB graph authentication

# Connect to graph
url = "http://localhost:7474/db/data/"
authenticate("localhost:7474", neo4jUser, neo4jPass)
graph = Graph(url)

# Authentication for cypher package
connPar = "http://" + neo4jUser + ":" + neo4jPass + "@localhost:7474/db/data/"
```

Agregar restricciones de unicidad a la base de datos:


```python
# Add uniqueness constraints
graph.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (l:Link) ASSERT l.url IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (s:Source) ASSERT s.name IS UNIQUE;")
```

Construir una lista con las palabras clave para la búsqueda de tweets:


```python
# Query words
queries = ["aguada", "aguatero", "hebraica", "macabi", "finalesLUB", "juntosporlanovena", "vamossha", "finaleslub"]
```

Crear un archivo de texto vacío para adjuntar (escribir) los nombres de los usuarios de los tweets encontrados:


```python
# Open file connection to append usernames
ufile = open("usernames_{}.txt".format("aguada-hebraica"), "a")
```

Cargar script de comandos en Cypher como cadena de caracteres


```python
# Pass dict to Cypher and build query from cypher script file
with open('/home/guzman/Documentos/GitLab/ComplexNetworks/Cypher/queries-in-script.cypher') as query:
    query = query.read()

print(query)
```

Definir los parámetros para la búsqueda de los tweets:


```python
# Parameters
count = 100 # The number of tweets to return per page, up to a maximum of 100. Defaults to 15.
result_type = "mixed" # Include both popular and real time results in the response.
until = "2017-06-04" # Returns tweets created before the given date.
lang = "es" # Restricts tweets to the given language
since_id = -1 # Returns results with an ID greater than (that is, more recent than) the specified ID.
```

Definir una función para la búsqueda de tweets que contiene la función de búsqueda de tweets de la librería tweepy y recibe como parámetros las palabras clave de búsqueda y el ID.


```python
def search_tweets(query, since_id):
    return api.search(q=query, count=count, until=until, result_type=result_type, lang=lang, since_id=since_id)
```

Iterar buscando tweets a partir de las palabras claves en la búsqueda y ejecutando el código importado en Cypher para insertar los registros en la base de datos no relacional de Neo4j.


```python
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
```

Import graph to python


```python
# Import graph to python - queries
# https://nicolewhite.github.io/neo4j-jupyter/hello-world.html

# Return all the nodes in the DB
# data = graph.run('')

data = graph.run('MATCH usPostw=(:User)-[r:POSTS]->(:Tweet) \
                  MATCH twRettw=(:Tweet)-[r2:RETWEETS]->(:Tweet) \
                  MATCH twReptw=(:Tweet)-[r3:REPLY_TO]->(:Tweet) \
                  MATCH twMenus=(:Tweet)-[r4:MENTIONS]->(:User) \
                  RETURN usPostw,twRettw,twReptw,twMenus \
                  LIMIT 10000;')

data = [tuple(x) for x in data]

# View first five graphs
i = 0
for i in range(0,5):
    print(str(i + 1) + " - " + str(data[i]) + "\n")
    i = i + 1
```

    1 - ((e7d8479)-[:POSTS]->(cf0a24e), (f949b73)-[:RETWEETS]->(b306a18), (e06876d)-[:REPLY_TO]->(a03511b), (f949b73)-[:MENTIONS]->(e7d8479))

    2 - ((e7d8479)-[:POSTS]->(cf0a24e), (f949b73)-[:RETWEETS]->(b306a18), (e06876d)-[:REPLY_TO]->(a03511b), (f949b73)-[:MENTIONS]->(de94de1))

    3 - ((e7d8479)-[:POSTS]->(cf0a24e), (f949b73)-[:RETWEETS]->(b306a18), (e06876d)-[:REPLY_TO]->(a03511b), (b306a18)-[:MENTIONS]->(de94de1))

    4 - ((e7d8479)-[:POSTS]->(cf0a24e), (f949b73)-[:RETWEETS]->(b306a18), (e06876d)-[:REPLY_TO]->(a03511b), (e3cc96b)-[:MENTIONS]->(b91061a))

    5 - ((e7d8479)-[:POSTS]->(cf0a24e), (f949b73)-[:RETWEETS]->(b306a18), (e06876d)-[:REPLY_TO]->(a03511b), (bfc1894)-[:MENTIONS]->(b91061a))



Crear objeto de grafos a partir de consulta a la base de datos Neo4j y ver su información:


```python
# Query Neo4j
results = cypher.run('MATCH usPostw=(:User)-[r:POSTS]->(:Tweet) \
                      MATCH twRettw=(:Tweet)-[r2:RETWEETS]->(:Tweet) \
                      MATCH twReptw=(:Tweet)-[r3:REPLY_TO]->(:Tweet) \
                      MATCH twMenus=(:Tweet)-[r4:MENTIONS]->(:User) \
                      RETURN usPostw,twRettw,twReptw,twMenus \
                      LIMIT 100000;', conn=connPar)

# Create graph object from Neo4j
g = results.get_graph()

# View info
print(nx.info(g))
```

    100000 rows affected.
    Name:
    Type: MultiDiGraph
    Number of nodes: 267
    Number of edges: 366
    Average in degree:   1.3708
    Average out degree:   1.3708


Graficar el objeto de grafos:


```python
%matplotlib inline

# Create network layout for visualizations
spring_pos = nx.spring_layout(g)

# Plot graph
plt.axis("off")
nx.draw_networkx(g, pos = spring_pos, with_labels = False, node_size = 30)

```


![png](output_31_0.png)



```python
%matplotlib inline

d = nx.degree(g)

# Plot graph
plt.axis("off")
nx.draw_networkx(g, pos = spring_pos, with_labels = False, nodelist=d.keys(), node_size=[v * 30 for v in d.values()])

```


![png](output_32_0.png)


Ver nodos:


```python
# View first five nodes
i = 0
for i in range(0,5):
    print(str(i + 1) + "- " + str(g.nodes(data=True)[i]))
    i = i + 1
```

    1- ('0', {'favorites': 2, 'created_at': 'Wed May 31 21:03:11 +0000 2017', 'id': 870022870512152577, 'text': 'tamos ahí @sandynyordi #JuntosPorLaNovena https://t.co/x2kWrWLrS2', 'labels': ['Tweet']})
    2- ('1', {'favorites': 0, 'created_at': 'Wed May 31 21:14:07 +0000 2017', 'id': 870025622801838080, 'text': 'RT @KarinaAguatera: tamos ahí @sandynyordi #JuntosPorLaNovena https://t.co/x2kWrWLrS2', 'labels': ['Tweet']})
    3- ('2', {'favorites': 1, 'created_at': 'Wed May 31 21:24:58 +0000 2017', 'id': 870028352631054336, 'text': 'mi trabajo de parto duro menos q sacar las entradas para la última final. #JuntosPorLaNovena', 'labels': ['Tweet']})
    4- ('100', {'followers': 190, 'screen_name': 'KarinaAguatera', 'following': 964, 'name': '@JAKCARBONEROS', 'statuses': 1725, 'profile_image_url': 'http://pbs.twimg.com/profile_images/871221543908638720/x4FSyHJs_normal.jpg', 'location': 'montevideo', 'labels': ['User']})
    5- ('4', {'favorites': 1, 'created_at': 'Thu Jun 01 13:37:06 +0000 2017', 'id': 870272998175014913, 'text': '@jptaibo27 Noo Juampa no me hagas eso! se me cayo un idolo! #juntosporlanovena  #gocavs   Aguatero y Lebronista!!', 'labels': ['Tweet']})


Ver ejes:


```python
# View first five edges
i = 0
for i in range(0,5):
    print(str(i + 1) + "- " + str(g.edges(data=True)[i]))
    i = i + 1
```

    1- ('0', '101', {'type': 'MENTIONS'})
    2- ('1', '100', {'type': 'MENTIONS'})
    3- ('1', '0', {'type': 'RETWEETS'})
    4- ('1', '101', {'type': 'MENTIONS'})
    5- ('100', '2', {'type': 'POSTS'})


Calcular principales métricas de los grafos:


```python
# Tipe of graph
esMultigrafo = g.is_multigraph()
esDireccional = g.is_directed()
esConectado = nx.is_connected(g2)

# Number of nodes and edges
numNod = nx.number_of_nodes(g)
numEdg = nx.number_of_edges(g)

# Degrees (max, min, mean)
deg = nx.degree(g)
in_degrees  = g.in_degree()
out_degrees  = g.out_degree()

# Componentes conectados
if not esConectado:
    g2 = g.to_undirected() # saco direccionalidad
    g3 = nx.connected_components(g2) # me quedo con componentes conectados

conComp = nx.number_connected_components(g2)

g2_components = nx.connected_component_subgraphs(g2)

# Componentes conexas
#cns = nx.connected_components(g)

# Diámetro
#d = nx.diameter(g)

# Excentricidad
#ecc = nx.eccentricity(g)

# Centro
#cen = nx.center(g)

# Periferia
#per = nx.periphery(g)

# Transistividad
#tr = nx.transitivity(g)

# Resumen
print("| -------------------------------------------- |")
if esMultigrafo:
    print("| Tipo de grafo: multigrafo")
if  not esMultigrafo:
    print("| Tipo de grafo: simple")

if esDireccional:
    print("| Direccional: si")
if  not esDireccional:
    print("| Direccional: no")

if esConectado:
    print("| Conectado: si")
if  not esConectado:
    print("| Conectado: no")
print("| -------------------------------------------- |")
print("| Número de nodos:", str(numNod))
print("| Número de conexiones:", str(numEdg))
print("| -------------------------------------------- |")
print("| Grado máximo entrada:", str(max(in_degrees.values())))
print("| Grado mínimo entrada:", str(min(in_degrees.values())))
print("| Grado promedio entrada:", str(sum(in_degrees.values())/len(deg.values())))
print("| -------------------------------------------- |")
print("| Grado máximo salida:", str(max(out_degrees.values())))
print("| Grado mínimo salida:", str(min(out_degrees.values())))
print("| Grado promedio salida:", str(sum(out_degrees.values())/len(deg.values())))
print("| -------------------------------------------- |")
print("| Grado máximo (no dir):", str(max(deg.values())))
print("| Grado mínimo (no dir):", str(min(deg.values())))
print("| Grado promedio (no dir):", str(sum(deg.values())/len(deg.values())))
print("| -------------------------------------------- |")
print("| Número de componentes conectados: %d" % nx.number_connected_components(g2))

#print("| Radio: %d" % nx.radius(g))
#print("| Diámetro: %d" % nx.diameter(g))
#print("| Excentricidad: %s" % nx.eccentricity(g))
#print("| Centro: %s" % center(g))
#print("| Periferia: %s" % periphery(g))
#print("| Densidad: %s" % density(g))
```

    | -------------------------------------------- |
    | Tipo de grafo: multigrafo
    | Direccional: si
    | Conectado: no
    | -------------------------------------------- |
    | Número de nodos: 267
    | Número de conexiones: 366
    | -------------------------------------------- |
    | Grado máximo entrada: 34
    | Grado mínimo entrada: 0
    | Grado promedio entrada: 1.3707865168539326
    | -------------------------------------------- |
    | Grado máximo salida: 6
    | Grado mínimo salida: 0
    | Grado promedio salida: 1.3707865168539326
    | -------------------------------------------- |
    | Grado máximo (no dir): 34
    | Grado mínimo (no dir): 1
    | Grado promedio (no dir): 2.741573033707865
    | -------------------------------------------- |
    | Número de componentes conectados: 38



```python
# Select most output connected nodes

#resultsDeg = cypher.run('MATCH usPostw=(n:User)-[r:POSTS]->(:Tweet) \
#                         RETURN id(n), size((n)-->()) as degree \
#                         ORDER BY degree DESC LIMIT 10;', conn=connPar)

#resultsDeg = cypher.run('MATCH (:Tweet)-[r4:MENTIONS]->(n:User) \
#                         RETURN id(n), size((n)-->()) as degree \
#                         ORDER BY degree DESC LIMIT 10;', conn=connPar)

#print(resultsDeg)

# Create graph object from Neo4j
#g = results.get_graph()
```

Detectar comunidades:


```python
import community

#parts = community.best_partition(g2)
#values = [parts.get(node) for node in g.nodes()]

#plt.axis("off")
#nx.draw_networkx(g, pos = spring_pos, cmap = plt.get_cmap("jet"), node_color = values, node_size = 35, with_labels = False)

```
