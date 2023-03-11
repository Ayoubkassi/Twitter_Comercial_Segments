import pandas as pd
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# Read the CSV file into a pandas dataframe
df = pd.read_csv('../data/i_want_an_iphone_after_+10500.csv')
# print(df)

# Connect to a MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=os.getenv("MYSQL_PASSWORD"),
    database='Twitter_Scrap'
)

# Convert the dataframe to a MySQL table
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Want_iphone')
cursor.execute(
    'CREATE TABLE Want_iphone (Username VARCHAR(16), Name VARCHAR(50), PostDate VARCHAR(25), TweetText VARCHAR(424), ReplyCount VARCHAR(25),RetweetCount VARCHAR(25),LikeCount VARCHAR(25),Views VARCHAR(25) )')
for row in df.itertuples():
    if row != None:
        print(1)
        cursor.execute(
            'INSERT INTO Want_iphone (Username, Name, PostDate, TweetText , ReplyCount ,RetweetCount ,LikeCount ,Views ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s )', tuple(row[1:]))
conn.commit()

# Close the connection
conn.close()
