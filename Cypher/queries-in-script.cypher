UNWIND {tweets} AS t

WITH t
ORDER BY t.id

WITH t,
t.entities AS e,
t.user AS u,
t.retweeted_status AS retweet

MERGE (tweet:Tweet {id:t.id})
SET tweet.text = t.text,
tweet.created_at = t.created_at,
tweet.favorites = t.favorite_count

MERGE (user:User {screen_name:u.screen_name})
SET user.name = u.name,
user.location = u.location,
user.followers = u.followers_count,
user.following = u.friends_count,
user.statuses = u.statuses_count,
user.profile_image_url = u.profile_image_url

MERGE (user)-[:POSTS]->(tweet)

MERGE (source:Source {name:t.source})
MERGE (tweet)-[:USING]->(source)

FOREACH (h IN e.hashtags |
  MERGE (tag:Hashtag {name:LOWER(h.text)})
  MERGE (tag)-[:TAGS]->(tweet)
  )

  FOREACH (u IN e.urls |
    MERGE (url:Link {url:u.expanded_url})
    MERGE (tweet)-[:CONTAINS]->(url)
    )

    FOREACH (m IN e.user_mentions |
      MERGE (mentioned:User {screen_name:m.screen_name})
      ON CREATE SET mentioned.name = m.name
      MERGE (tweet)-[:MENTIONS]->(mentioned)
      )

      FOREACH (r IN [r IN [t.in_reply_to_status_id] WHERE r IS NOT NULL] |
        MERGE (reply_tweet:Tweet {id:r})
        MERGE (tweet)-[:REPLY_TO]->(reply_tweet)
        )

        FOREACH (retweet_id IN [x IN [retweet.id] WHERE x IS NOT NULL] |
          MERGE (retweet_tweet:Tweet {id:retweet_id})
          MERGE (tweet)-[:RETWEETS]->(retweet_tweet)
          )
