import pandas as pd
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# Read the CSV file into a pandas dataframe
df = pd.read_csv('../apple.csv')
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
cursor.execute('DROP TABLE IF EXISTS apple')
cursor.execute(
    'CREATE TABLE apple (Username VARCHAR(16), Name VARCHAR(50), PostDate VARCHAR(25), TweetText VARCHAR(424), ReplyCount VARCHAR(25),RetweetCount VARCHAR(25),LikeCount VARCHAR(25),Views VARCHAR(25), gender VARCHAR(10) )')
for row in df.itertuples():
    cursor.execute(
        'INSERT INTO apple (Username, Name, PostDate, TweetText , ReplyCount ,RetweetCount ,LikeCount ,Views , gender ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s )', tuple(row[1:]))
conn.commit()

# Close the connection
conn.close()
