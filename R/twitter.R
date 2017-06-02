
# Load libraries ----------------------------------------------------------

library('twitteR')
library('igraph')
library('ggplot2') # plots
library('dismo') # geocoding

# library(lubridate)
# library(RJSONIO)
# library(dismo)
# library(maps)


# OAauth ------------------------------------------------------------------

# https://apps.twitter.com/
# https://www.r-bloggers.com/setting-up-the-twitter-r-package-for-text-analytics/

# OAUth
# setup_twitter_oauth(
#   consumer_key = "",
#   consumer_secret = "",
#   access_token = "",
#   access_secret = ""
# )

source(file = "twitter-OAuth.R")

# Get Followers/Follows data ----------------------------------------------

# Look up for the users
elPais <- lookupUsers("elpaisuy")
laDiaria <- lookupUsers("ladiaria")

# Get data from the users
elPais$elpaisuy$created
elPais$elpaisuy$description
elPais$elpaisuy$followersCount # 529951
elPais$elpaisuy$friendsCount # 438
elPais$elpaisuy$location

# Friends
elPaisFriends <- elPais$elpaisuy$getFriends() # who this user follows
elPaisFriends.df <- twListToDF(elPaisFriends)

laDiariaFriends <- laDiaria$ladiaria$getFriends() # who this user follows
laDiariaFriends.df <- twListToDF(laDiariaFriends)

# Followers

elPaisFollowers <- elPais$elpaisuy$getFollowers(retryOnRateLimit = 200) # who follows this user
elPaisFollowers.df <- twListToDF(elPaisFollowers)

laDiariaFollowers <- laDiaria$ladiaria$getFollowers(retryOnRateLimit = 200) # who follows this user
laDiariaFollowers.df <- twListToDF(laDiariaFollowers)


elPaisFollowers.df2 = data.table::rbindlist(lapply(elPaisFollowers,as.data.frame))


# Write data to file ------------------------------------------------------

write.csv(elPaisFriends.df, "elPaisFriends.csv", sep = ",")
write.csv(laDiariaFriends.df, "laDiariaFriends.csv", sep = ",")
write.csv(elPaisFollowers.df, "elPaisFollowers.csv", sep = ",")
write.csv(laDiariaFollowers.df, "laDiariaFollowers.csv")

# a follower's followers
# followers2 <- followers[[1]]$getFollowers()

# Relations
relations <- merge(data.frame('User' = elPais$elpaisuy$screenName,
                              'Follower' = elPaisFriends.df$screenName),
                   data.frame('User' = elPaisFollowers.df$screenName,
                              'Follower' = elPais$elpaisuy$screenName), all = TRUE)

# Create graph from relations df
g <- graph.data.frame(relations[1:50,], directed = TRUE)

# Remove loops
g <- simplify(g)

# set labels and degrees of vertices
V(g)$label <- V(g)$name

g # print

# set seed to make the layout reproducible
set.seed(3952)
layout1 <- layout.fruchterman.reingold(g)

plot(g, layout = layout1)

# Better plot
V(g)$label.cex <- 2.2 * V(g)$degree / max(V(g)$degree) + 0.2
V(g)$label.color <- rgb(0, 0, 0.2, 0.8)
V(g)$frame.color <- NA
egam <- (log(E(g)$weight) + 0.4) / max(log(E(g)$weight) + 0.4)
E(g)$color <- rgb(0.5, 0.5, 0, egam)
E(g)$width <- egam

# plot the graph in layout1
plot(g, layout = layout1)


# Get tweets data ---------------------------------------------------------

# Get tweets (3200 is the maximum to retrieve)
tweetsElPais <- userTimeline("elpaisuy", n = 3200)
tweetsLaDiaria <- userTimeline("laDiaria", n = 3200)
tweetsElObservador <- userTimeline("ElObservador", n = 3200)

# Convert to data frame
tweetsElPais.df <- twListToDF(tweetsElPais)
tweetsLaDiaria.df <- twListToDF(tweetsLaDiaria)
tweetsElObservador.df <- twListToDF(tweetsElObservador)

# Check head
head(tweetsElPais.df)


