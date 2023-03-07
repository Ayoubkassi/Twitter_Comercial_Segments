from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
from dotenv import load_dotenv
import json
import requests
from selenium.webdriver.common.by import By


load_dotenv()


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

    def getTweets(self, username, password, nbPage=20):
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
        last_url = "&src=typed_query&f=live"
        words = self.words
        if len(words) != 0:
            for i in range(0, len(words) - 1):
                first_url += words[i] + "%20"
            first_url += words[-1]

        url = first_url + last_url

        sleep(3)
        driver.get(url)
        sleep(5)
        data = {}
        twitter_names = []
        twitter_usernames = []
        twitter_post_date = []
        twitter_tweets = []
        twitter_replies = []
        twitter_retweets = []
        twitter_likes = []
        twitter_views = []
        i = 0
        for i in range(nbPage):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            sleep(1)
            cards = driver.find_elements("xpath", '//article[@data-testid="tweet"]')
            for card in cards:
                print(i)
                try:
                    name = card.find_element(
                        "xpath",
                        "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span",
                    ).text
                    twitter_names.append(name)
                    # print(name.text)
                    username = card.find_element(
                        "xpath",
                        "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span",
                    ).text
                    twitter_usernames.append(username)

                    posted_at = card.find_element(
                        "xpath",
                        "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time",
                    ).text
                    twitter_post_date.append(posted_at)

                    # likes
                    likes = card.find_element(
                        By.XPATH,
                        "./div/div/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/span/span/span",
                    ).text
                    print("likes :" + likes)

                    # replies
                    retweets = card.find_element(
                        By.XPATH,
                        "./div/div/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]/span/span/span",
                    ).text

                    # retweets
                    replies = card.find_element(
                        By.XPATH,
                        "./div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span",
                    ).text

                    views = card.find_element(
                        By.XPATH,
                        "./div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span/span/span",
                    ).text

                    try:
                        twitter_likes.append(likes)
                    except:
                        twitter_likes.append("0")
                    try:
                        twitter_replies.append(replies)
                    except:
                        twitter_replies.append("0")
                    try:
                        twitter_retweets.append(retweets)
                    except:
                        twitter_retweets.append("0")
                    try:
                        twitter_views.append(views)
                    except:
                        twitter_views.append("0")

                    try:
                        tweets = card.find_elements(
                            "xpath",
                            "./div/div/div[2]/div[2]/div[3]/div",
                        )

                        tweet_text = ""
                        tweets_div = card.find_element(
                            By.XPATH, "./div/div/div[2]/div[2]/div[2]/div"
                        )
                        spans = tweets_div.find_elements(By.TAG_NAME, "span")
                        for span_test in spans:
                            tweet_text += span_test.text.strip() + " "

                        twitter_tweets.append(tweet_text)
                    except:
                        twitter_tweets.append("Empty")

                except:
                    print("########################00")

                i += 1

        sleep(5)

        data["names"] = twitter_names
        data["usernames"] = twitter_usernames
        data["posted_date"] = twitter_post_date
        data["replies"] = twitter_replies
        data["retweets"] = twitter_retweets
        data["likes"] = twitter_likes
        data["views"] = twitter_views
        data["tweets"] = twitter_tweets

        with open(project + ".json", "w") as f:
            json.dump(data, f)

    def scrapUsers(self):
        f = open("iphone.json")
        data = json.load(f)
        users = data["usernames"]
        # download html files
        for user in users:
            # start scraping
            url = "https://twitter.com/" + user
            # we must use selenium bcs twitter first page is lazy loading that use javascript code to render content
            driver = webdriver.Chrome()
            driver.get(url)
            sleep(1)
            html = driver.page_source
            file = open("profiles/" + user + ".html", "w")
            # Write the data to the file
            file.write(html)
            # Close the file
            file.close()

        twitter_users = []
        for user in users:
            twitter_user = {}
            with open(project + "/" + user + ".html") as file:
                html = file.read()
            soup = BeautifulSoup(html, "html.parser")
            try:
                script = soup.find(
                    "script", {"data-testid": "UserProfileSchema-test"}
                ).string
                data = json.loads(str(script))
            except:
                pass
            try:
                twitter_user["type"] = data["@type"]
            except:
                pass
            try:
                twitter_user["dateCreated"] = data["dateCreated"]
            except:
                pass
            try:
                twitter_user["username"] = data["author"]["additionalName"]
            except:
                pass
            try:
                twitter_user["givenName"] = data["author"]["givenName"]
            except:
                pass
            try:
                twitter_user["description"] = data["author"]["description"]
            except:
                pass
            try:
                twitter_user["location"] = data["author"]["homeLocation"]["name"]
            except:
                pass
            try:
                twitter_user["id"] = data["author"]["identifier"]
            except:
                pass
            try:
                twitter_user["follows"] = data["author"]["interactionStatistic"][0][
                    "userInteractionCount"
                ]
            except:
                pass
            try:
                twitter_user["friends"] = data["author"]["interactionStatistic"][1][
                    "userInteractionCount"
                ]
            except:
                pass
            try:
                twitter_user["tweets"] = data["author"]["interactionStatistic"][2][
                    "userInteractionCount"
                ]
            except:
                pass

            twitter_users.append(twitter_user)
        with open(project + "_users.json", "w") as f:
            json.dump(twitter_users, f)


# project = input("What is the name of your project : ")
# n = int(input("Entrer le nomre de page : "))
# words = []
# takeValue = True
# while takeValue:
#     words.append(input("Enter a keyword : "))
#     a = input("Add new keyword (Y/N) : ").lower()
#     if a == "y":
#         takeValue = True
#     else:
#         takeValue = False

words = []
project = "iphone"

twitter_bot = TwitterAdvancedSearch(words)
password = os.getenv("PASSWORD")
# twitter_bot.getTweets("KraceAyoub", password, n)
twitter_bot.scrapUsers()
