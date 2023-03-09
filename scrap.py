from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from time import sleep
import json
import os
import csv
from dotenv import load_dotenv


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

    def login_to_twitter(self, username, password, nbPage=2):
        try:
            twitter_login = "https://twitter.com/login"
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

        except exceptions.TimeoutException:
            print("Timeout while waiting for Login screen")
            return False

        return True

    def enter_search_data(self, driver):
        # get the link with the required params
        first_url = "https://twitter.com/search?q="
        last_url = "&src=typed_query"
        words = self.words
        if len(words) != 0:
            for i in range(0, len(words) - 1):
                first_url += words[i] + "%20"
            first_url += words[-1]
        url = first_url + last_url
        driver.get(url)
        sleep(5)

        return True

    def collect_all_tweets_articles(self, driver):
        cards = driver.find_elements(
            "xpath", '//article[@data-testid="tweet"]')
        return cards

    def get_data_artcile(self, card):

        try:
            name = card.find_element(
                "xpath",
                "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span",
            ).text
        except exceptions.NoSuchElementException:
            name = ""

        try:
            username = card.find_element(
                "xpath",
                "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span",
            ).text
        except exceptions.NoSuchElementException:
            username = ""

        try:
            posted_at = card.find_element(
                "xpath",
                "./div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a/time",
            ).text
        except exceptions.NoSuchElementException:
            posted_at = ""

        try:
            likes = card.find_element(
                By.XPATH,
                "./div/div/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/span/span/span",
            ).text
        except exceptions.NoSuchElementException:
            likes = ""

        try:
            retweets = card.find_element(
                By.XPATH,
                "./div/div/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]/span/span/span",
            ).text

        except exceptions.NoSuchElementException:
            retweets = ""

        try:
            views = card.find_element(
                By.XPATH,
                "./div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span/span/span",
            ).text
        except exceptions.NoSuchElementException:
            views = ""

        try:
            replies = card.find_element(
                By.XPATH,
                "./div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span",
            ).text
        except exceptions.NoSuchElementException:
            replies = ""

        tweet_text = ""
        try:
            tweets_div = card.find_element(
                By.XPATH, "./div/div/div[2]/div[2]/div[2]/div"
            )
            spans = tweets_div.find_elements(By.TAG_NAME, "span")
            for span_test in spans:
                tweet_text += span_test.text.strip() + " "
            twitter_tweets = tweet_text

        except exceptions.NoSuchElementException:
            twitter_tweets = ""

        tweet = (
            username,
            name,
            posted_at,
            twitter_tweets,
            replies,
            retweets,
            likes,
            views
        )
        return tweet

    def generate_tweet_id(self, tweet):
        return "".join(tweet)

    def save_record_to_file(self, record, filename):
        filename += "_users.json"
        with open(filename, 'a') as f:
            json.dump(record, f)
            f.write('\n')

    def save_tweet_data_to_csv(self, records, project, mode="a+"):
        header = [
            "Username",
            "Name",
            "PostDate",
            "TweetText",
            "ReplyCount",
            "RetweetCount",
            "LikeCount",
            "Views",
        ]
        project += ".csv"
        with open(project, mode=mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if mode == "w":
                writer.writerow(header)
            if records:
                writer.writerow(records)

    def main(self, user, password, nb_page, project):
        driver = webdriver.Chrome()
        self.save_tweet_data_to_csv(None, project, "w")
        login = self.login_to_twitter(user, password, nb_page)
        if not login:
            return False
        self.enter_search_data(driver)
        unique_tweets = set()

        for i in range(nb_page):
            articles = self.collect_all_tweets_articles(driver)
            sleep(1)
            articles = driver.find_elements(
                "xpath", '//article[@data-testid="tweet"]')
            for article in articles:
                try:
                    tweet = self.get_data_artcile(article)
                except exceptions.StaleElementReferenceException:
                    continue
                if not tweet:
                    continue
                tweet_id = self.generate_tweet_id(tweet)
                if tweet_id not in unique_tweets:
                    unique_tweets.add(tweet_id)
                    self.save_tweet_data_to_csv(tweet, project)

            driver.execute_script(
                "window.scrollBy(0, document.body.scrollHeight);")

        driver.quit()

    def scrapUsers(self, project):
        users = []
        with open(project + ".csv") as csvfile:
            csvreader = csv.reader(csvfile)
            i = 0
            for row in csvreader:
                if i == 0:
                    i += 1
                    continue
                users.append(row[0][1:])

        # download html files
        twitter_users = {}
        for user in users:
            # start scraping
            # if os.path.isfile("profiles/" + user + ".html"):
            #     continue
            url = "https://twitter.com/" + user
            # we must use selenium bcs twitter first page is lazy loading that use javascript code to render content
            driver = webdriver.Chrome()
            driver.get(url)
            sleep(1)
            # html = driver.page_source
            # file = open("profiles/" + user + ".html", "w")
            # # Write the data to the file
            # file.write(html)
            # # Close the file
            # file.close()

            # get and store data
            twitter_user = {}
            try:
                script_content = driver.execute_script(
                    "return document.querySelector('html head script:nth-of-type(2)').textContent")
                data = json.loads(str(script_content))
                id = data["author"]["identifier"]
                print(id)
                if id in twitter_users:
                    continue
                else:
                    twitter_user["type"] = data["@type"]
                    try:
                        twitter_user["dateCreated"] = data["dateCreated"]
                    except:
                        pass
                    twitter_user["username"] = data["author"]["additionalName"]
                    twitter_user["givenName"] = data["author"]["givenName"]
                    try:
                        twitter_user["description"] = data["author"]["description"]
                    except:
                        pass
                    try:
                        twitter_user["location"] = data["author"]["homeLocation"]["name"]
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

                    # print(twitter_user)
                    twitter_users[id] = twitter_user
                    self.save_record_to_file(twitter_user, project)
            except:
                pass

        # with open(project + "_users.json", "w") as f:
        #     json.dump(twitter_users, f)


if __name__ == "__main__":
    user = "KraceAyoub"
    password = os.getenv("PASSWORD")
    nb_page = 2
    words = ["naruto"]
    project = "apple"
    twitter_bot = TwitterAdvancedSearch(words)
    # twitter_bot.main(user, password, nb_page, project)
    twitter_bot.scrapUsers(project)
