from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from time import sleep
import json
import os
import csv
from dotenv import load_dotenv
import threading
from datetime import date

load_dotenv()


class TwitterAdvancedSearch:
    def __init__(
        self,
        words=[],
        project="",
        exact_phrase="",
        none_words="",
        hashtags=[],
        min_replies=0,
        min_likes=0,
        min_retweets= 0,
        from_date="2006-01-01",
        to_date= str(date.today()),
    ):
        self.words = words
        self.project = project
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
        last_url = '&src=typed_query'
        
        words = self.words
        if len(words) != 0:
            for i in range(0, len(words) - 1):
                first_url += words[i] + "%20"
            first_url += words[-1]

        # add exact phrase
        second_url = ""
        exact_phrase_words = ""
        phrase = self.exact_phrase.strip().split()
        if len(phrase) != 0:
            for i in range(0, len(phrase) - 1):
                second_url += phrase[i] + "%20"
            second_url += phrase[-1]
            exact_phrase_words = second_url
            exact_phrase_words += '%20"'
            exact_phrase_words = '"' + exact_phrase_words

        # none words
    
        third_url = ""
        none_words = self.none_words
        if len(none_words) != 0:
            third_url = "%20-"
            for i in range(0, len(none_words) - 1):
                third_url += none_words[i] + "%20-"
            third_url += none_words[-1]

        # min_replies%3A20%20min_faves%3A30%20min_retweets%3A40
        min_replies = self.min_replies
        min_faves = self.min_likes
        min_retweets = self.min_retweets

        fourd_url = "%20min_replies%3A"+str(min_replies) + "%20min_faves%3A" + str(
            min_faves) + "%20min_retweets%3A" + str(min_retweets)

        # until%3A2011-06-15%20since%3A2011-03-16
        from_date = self.from_date
        until_date = self.to_date
        five_url = "%20until%3A" + until_date + "%20since%3A" + from_date

        url = first_url + exact_phrase_words + \
            third_url + fourd_url + five_url + last_url

        url += "&f=live"
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
        with open("data/"+filename, 'a') as f:
            json.dump(record, f)
            f.write(',\n')

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
        with open("data/"+project, mode=mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if mode == "w":
                writer.writerow(header)
            if records:
                writer.writerow(records)

            
                  
    def main(self, user, password, nb_page, project):
        driver = webdriver.Chrome()
        self.save_tweet_data_to_csv(None, project, "w")
        # login = self.login_to_twitter(user, password, nb_page)
        # if not login:
        #     return False
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
        i = 0
        for user in users:
            # start scraping
            # if os.path.isfile("profiles/" + user + ".html"):
            #     continue
            url = "https://twitter.com/" + user
            # we must use selenium bcs twitter first page is lazy loading that use javascript code to render content
            if i == 0:
                driver = webdriver.Chrome()
                driver.get(url)
                i += 1
            else:
                # html = driver.page_source
                # file = open("profiles/" + user + ".html", "w")
                # # Write the data to the file
                # file.write(html)
                # # Close the file
                # file.close()

                # get and store data
                scriptLink = "window.location.href = '{}';".format(url)
                driver.execute_script(scriptLink)

            twitter_user = {}
            try:
                sleep(1)
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

                    twitter_users[id] = twitter_user
                    self.save_record_to_file(twitter_user, project)
            except:
                pass

    # Scrapping users using multithreading for a faster scrapping

    def scrapUsers2(self, users):
        twitter_users = {}
        i = 0
        project = self.project
        for user in users:

            #     continue
            url = "https://twitter.com/" + user
            # we must use selenium bcs twitter first page is lazy loading that use javascript code to render content
            if i == 0:
                driver = webdriver.Chrome()
                driver.get(url)
                i += 1
            else:

                # get and store data
                scriptLink = "window.location.href = '{}';".format(url)
                driver.execute_script(scriptLink)

            twitter_user = {}
            try:
                sleep(1)
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

                    twitter_users[id] = twitter_user
                    # print(twitter_user)
                    self.save_record_to_file(twitter_user, project)
            except:
                pass

    def fixing_json_problem(self, project):
        # Open the JSON file in read mode
        with open("data/" + project + '_users' + '.json', 'r') as f:
            # Read the contents of the file
            contents = f.read()

        # Remove the comma at the end of the last JSON object
        contents = contents[:-2] if contents.endswith(',\n') else contents

        # Add "[" at the beginning and "]" at the end of the contents
        new_contents = '[' + contents + ']'

        # Open the same file in write mode
        with open("data/" + project + '_users' + '.json', 'w') as f:
            # Write the modified contents back to the file
            f.write(new_contents)

        # Close the file
        f.close()


if __name__ == "__main__":
    user = "amineloco5"
    # password = os.getenv("PASSWORD")
    nb_page = 10
    words = []
    exact_phrase_words = ""
    none_words = []
    project = input("What is the name of your project : ")
    takeValue = True
    from_date = ""
    to_date = ""
        
    askwords = input("Enter a keywords, if many seperate them with a comma  ',': ")
    words.extend(askwords.split(","))
    
    
    ask_exact_phrase_words = input("Add an exacte phrase ?(Y/N): ").lower()
    if ask_exact_phrase_words == 'y':
        exact_phrase_words = input("Add an exacte phrase : ").lower()
    else:
        exact_phrase_words = ""

    asknone_words = input("Add none words (Y/N): ")
    if asknone_words == 'y':
        get_none_words = input("Add none words, if many seperate them with a comma ','  ").lower()
        none_words.extend(get_none_words.split(","))
    else:
        none_words = []
        
    askfordat = input("Do you want to search within a timeline ? (Y/N): ").lower()
    if askfordat == 'y':
        from_date = input("from which date  (date format : YYYY-MM-DD ) : ")
        to_date = input("to which date  (date format : YYYY-MM-DD ) : ")
    else:
        from_date = "2006-01-01"
        to_date = str(date.today())
        
    aksForReplies = input("Do you want to specify minimum replies ? (Y/N): ").lower()
    if aksForReplies == 'y':
        min_replies = int(input(" How many minimum replies : "))
    else:
        min_replies = 0
        
    aksForLikes = input("Do you want to specify minimum likes ? (Y/N): ").lower()
    if aksForLikes == 'y':
        min_likes = int(input("How many minimum likes : "))
    else:
        min_likes = 0
    
    aksForRetweets = input("Do you want to specify minimum retweets ? (Y/N): ").lower()
    if aksForRetweets == 'y':
        min_retweets = int(input("How many minimum retweets : "))
    else:
        min_retweets = 0
    
    number_of_tweets = int(input("what's the max number of pages you wanna scroll : "))
    
    if from_date == "" and to_date == "":
        twitter_bot = TwitterAdvancedSearch(
        words=words, project=project, none_words=none_words, exact_phrase=exact_phrase_words, min_likes=min_likes, min_replies=min_replies,min_retweets=min_retweets)
    else :
        twitter_bot = TwitterAdvancedSearch(
        words=words, project=project, none_words=none_words, exact_phrase=exact_phrase_words, from_date=from_date, to_date=to_date, min_likes=min_likes, min_replies=min_replies,min_retweets=min_retweets)
    
    
    twitter_bot.main(user, "Amine-1963", number_of_tweets, project)

    # scrapping users without multithreading
    # twitter_bot.scrapUsers(project)

    # create threads for each set of arguments

    users = []
    with open("data/" + project + ".csv") as csvfile:
        csvreader = csv.reader(csvfile)
        i = 0
        for row in csvreader:
            if i == 0:
                i += 1
                continue
            users.append(row[0][1:])

    args_lists = []
    lengh_args = len(users) // 8
    args_lists.append(users[:lengh_args])
    args_lists.append(users[lengh_args:2*lengh_args])
    args_lists.append(users[2*lengh_args:3*lengh_args])
    args_lists.append(users[3*lengh_args:4*lengh_args])
    args_lists.append(users[4*lengh_args:5*lengh_args])
    args_lists.append(users[5*lengh_args:6*lengh_args])
    args_lists.append(users[6*lengh_args:7*lengh_args])
    args_lists.append(users[7*lengh_args:])

    threads = []
    for args in args_lists:
        # print("args")
        # print(type(args))
        thread = threading.Thread(target=twitter_bot.scrapUsers2, args=(args,))
        threads.append(thread)

    # start all the threads
    for thread in threads:
        thread.start()

    # wait for all the threads to finish
    for thread in threads:
        thread.join()

    twitter_bot.fixing_json_problem(project)

    # https://twitter.com/search?q=%22i%20want%20an%20iphone%22%20min_replies%3A10%20min_faves%3A10%20min_retweets%3A5%20until%3A2023-03-11%20since%3A2006-01-01&src=typed_query&f=live


# https://twitter.com/search?q=iphone%22iphone%20%22%20min_replies%3A10%20min_faves%3A10%20min_retweets%3A10%20until%3A2013-03-02%20since%3A2023-03-11&src=typed_query


# https://twitter.com/search?f=top&q=iphone%20%22iphone%22%20min_replies%3A10%20min_faves%3A10%20min_retweets%3A10%20until%3A2021-08-15%20since%3A2014-06-17&src=typed_query
