import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(buy iphone) until:2022-03-09 since:2022-03-01"
tweets = []
limit = 500

for tweet in sntwitter.TwitterSearchScraper(query).get_items():

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.username, tweet.user, tweet.date, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.viewCount])

df = pd.DataFrame(tweets, columns=['username', 'Profile', 'Date', 'Tweet', 'ReplyCount', 'RetweetCount', 'LikeCount', 'ViewCount'])
print(df)


# to save to csv
df.to_csv('tweets.csv')
