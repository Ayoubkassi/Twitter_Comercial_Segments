import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd


def getNames():
    # different genders and their corresponding number of pages
    genders = {"female": ["feminine", 41], "male": ["masculine", 50]}
    data = {}
    for key, val in genders.items():
        my_names = []
        for i in range(1, val[1]):
            url = "https://www.behindthename.com/names/gender/" + \
                val[0] + "/" + str(i)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            names = soup.find_all("a", {"class": "nll"})
            my_names.extend([name.text for name in names])
        data[key] = my_names
    return data


def get_new_column(filename):
    gender = []
    with open('names.json', 'r') as json_file:
        names_data = json.load(json_file)
    with open("../data/" + filename + ".csv") as csvfile:
        csvreader = csv.reader(csvfile)
        i = -1
        for row in csvreader:
            i += 1
            if (i == 0):
                i += 1
                gender.append("uknown")
                continue
            names = row[3].split()
            for name in names:
                if name.capitalize() in names_data:
                    gender.append(names_data[name.capitalize()])
                    break
                else:
                    gender.append("uknown")
                    break

    return gender


def add_column(filename, column_name):
    new_column_data = get_new_column(filename)
    print(new_column_data)
    df = pd.read_csv("../data/"+filename+'.csv')
    df[column_name] = new_column_data[1:]
    df.to_csv('../data/'+ filename+ "with_gender" + '.csv', index=False)


add_column("apple_users", "gender")
