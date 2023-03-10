# Twitter Comercial Segments

---

**Twitter General Multi Threaded Scrapper With Selenium and Beautifoul-Soup**

We presented this project (initally a class project) to our fellow students (@IMT Mines Ales) today. You can check the presentation (in English) here:[Presentation Link](https://www.canva.com/design/DAFcvmVm-Nc/4B7Mo-JtfyUaU7TM-u5N1w/view?utm_content=DAFcvmVm-Nc&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

### Run Data Analysis in Colab To get some usefull infos about your business

![Data Analysis](analys_result.png)

A simple python script to scrap tweets and users , the object is to get the data ready for some analysis studies , we choose MySQL to be the database for our scrapped Data .

### Tweet Schema :

- Username
- Name
- PostDate
- TweetText
- ReplyCount
- RetweetCount
- LikeCount
- Views

# Usage

---

1. Clone

2. Install dependencies : pip install - r requirements.txt

3. create .env with the password of your twitter

4. Run docker container and create image :

```bash
docker image build -t twitter-scrap .
docker run twitter-scrap
```

Dockerhub repository : [Click Here](https://hub.docker.com/repository/docker/ayoubkassi/twitter-scrap/general)

#### To export mysql database :

> mysqldump -u YourUser -p YourDatabaseName > wantedsqlfile.sql

#### To export mongodb database :

> mongodump --db mydb --out backup/
