from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
from dotenv import load_dotenv
import json
import requests


load_dotenv()


# from get_gender import getNames
# import json
# import os

# data = getNames()

# with open("names.json", "w") as f:
#     json.dump(data, f)


class TwitterAdvancedSearch:
    def __init__(
        self,
        words=[],
        exact_phrase="",
        none_words=[],
        hashtags=[],
        min_replies=0,
        min_likes=0,
        min_retweets=0,
        from_date="02-03-2023",
        to_date="02-03-2023",
    ):
        self.words = words
        self.exact_phrase = exact_phrase
        self.none_words = none_words
        self.hashtags = hashtags
        self.min_replies = min_replies
        self.min_likes = min_likes
        self.min_retweets = min_retweets
        self.from_date = from_date
        self.to_date = to_date

    def getTweets(self, username, password):
        try:
            twitter_login = "https://twitter.com/i/flow/login"
            driver = webdriver.Chrome()
            driver.get(twitter_login)
            sleep(2)
            login_field = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input',
            ).send_keys(username)
            sleep(3)
            pre_login_butt = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span/span',
            ).click()
            sleep(3)
            pass_field = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
            ).send_keys(password)
            sleep(4)
            login_butt = driver.find_element(
                "xpath",
                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span',
            ).click()

            # get the link with the required params
            first_url = "https://twitter.com/search?q="
            last_url = "&src=typed_query"
            words = self.words
            if len(words) != 0:
                for i in range(0, len(words) - 1):
                    first_url += words[i] + "%20"
                first_url += words[-1]

            url = first_url + last_url

            sleep(3)
            driver.get(url)
            sleep(5)
            driver.execute_script("window.scrollBy(0, 50000);")
            sleep(3)
            html = driver.page_source
            file = open("scrap.html", "w")
            # Write the data to the file
            file.write(html)
            # Close the file
            file.close()
            # print(html)

        except:
            print("error occured!!")

    def scrapTweets(self):
        data = {}
        with open("scrap.html") as file:
            html = file.read()

        twitter_names = []
        twitter_usernames = []
        twitter_post_date = []
        twitter_tweets = []
        twitter_replies = []
        twitter_retweets = []
        twitter_likes = []
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")
        for articles in articles:
            # names
            username = articles.find("div", {"data-testid": "User-Names"})
            subnames = username.contents[0]
            name = subnames.find_all("span")[1].string
            twitter_names.append(name)

            # usernames
            identifier = username.contents[1]
            id = identifier.find("a")
            Id = id.find("span").string[1:]
            twitter_usernames.append(Id)

            # date
            post_date = identifier.find("time").string
            twitter_post_date.append(post_date)

            # tweet
            tweet_text = ""
            tweet_div = articles.find("div", {"data-testid": "tweetText"})
            tweets = tweet_div.find_all("span")
            for tweet in tweets:
                if tweet.string.strip() != "\n" and tweet.string.strip() != "":
                    tweet_text += tweet.string.strip() + " "

            twitter_tweets.append(tweet_text)

            # replys
            reply_div = articles.find("div", {"data-testid": "reply"})
            reply = reply_div.find_all("span")[-1].string
            if reply == None:
                reply = "0"
            twitter_replies.append(reply)

            # retweet
            retweet_div = articles.find("div", {"data-testid": "retweet"})
            retweet = reply_div.find_all("span")[-1].string
            if retweet == None:
                retweet = "0"
            twitter_retweets.append(retweet)

            # retweet
            like_div = articles.find("div", {"data-testid": "like"})
            like = reply_div.find_all("span")[-1].string
            if like == None:
                like = "0"
            twitter_likes.append(like)

        data["names"] = twitter_names
        data["usernames"] = twitter_usernames
        data["posted_date"] = twitter_post_date
        data["tweets"] = twitter_tweets
        data["replies"] = twitter_replies
        data["retweets"] = twitter_retweets
        data["likes"] = twitter_likes
        # usernames

        with open("tweets.json", "w") as f:
            json.dump(data, f)

    def scrapUsers(self):
        f = open("tweets.json")
        data = json.load(f)
        users = data["usernames"]
        # download html files
        # for user in users:
        #     # start scraping
        #     url = "https://twitter.com/" + user
        #     # we must use selenium bcs twitter first page is lazy loading that use javascript code to render content
        #     driver = webdriver.Chrome()
        #     driver.get(url)
        #     sleep(1)
        #     html = driver.page_source
        #     file = open("profiles/" + user + ".html", "w")
        #     # Write the data to the file
        #     file.write(html)
        #     # Close the file
        #     file.close()
        # soup = BeautifulSoup(response.content, "html.parser")
        # print(soup.prettify())

        # # localisation
        # localisation_container = soup.find_all("span")
        # print(localisation_container)

        # work with scrap again
        # data-testid="UserProfileSchema-test"
        twitter_users = []
        for user in users:
            twitter_user = {}
            with open("profiles/" + user + ".html") as file:
                html = file.read()
            soup = BeautifulSoup(html, "html.parser")
            script = soup.find(
                "script", {"data-testid": "UserProfileSchema-test"}
            ).string
            data = json.loads(str(script))
            twitter_user["type"] = data["@type"]
            twitter_user["dateCreated"] = data["dateCreated"]
            twitter_user["username"] = data["author"]["additionalName"]
            twitter_user["givenName"] = data["author"]["givenName"]
            twitter_user["description"] = data["author"]["description"]
            twitter_user["location"] = data["author"]["homeLocation"]["name"]
            twitter_user["id"] = data["author"]["identifier"]
            twitter_user["follows"] = data["author"]["interactionStatistic"][0][
                "userInteractionCount"
            ]
            twitter_user["friends"] = data["author"]["interactionStatistic"][1][
                "userInteractionCount"
            ]
            twitter_user["tweets"] = data["author"]["interactionStatistic"][2][
                "userInteractionCount"
            ]

            twitter_users.append(twitter_user)
        with open("users.json", "w") as f:
            json.dump(twitter_users, f)


# get html file
twitter_bot = TwitterAdvancedSearch(words=["iphone", "new"])
# password = os.getenv("PASSWORD")
# twitter_bot.getTweets("KraceAyoub", password)
# twitter_bot.scrapTweets()
twitter_bot.scrapUsers()
