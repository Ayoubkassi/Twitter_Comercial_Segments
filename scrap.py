from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
from dotenv import load_dotenv

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


twitter_bot = TwitterAdvancedSearch(words=["iphone", "new"])
password = os.getenv("PASSWORD")
twitter_bot.getTweets("KraceAyoub", password)
