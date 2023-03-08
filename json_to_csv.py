import json
import csv
import pandas as pd


def to_csv(filename):
    with open(filename+'.json', 'r') as json_file:
        data = json.load(json_file)

    with open(filename+'.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(data[0].keys())

        for row in data:
            writer.writerow(row.values())


def reformat_json(filename):
    with open(filename+'.json', 'r') as json_file:
        data = json.load(json_file)

    new_data = {}
    females = data["female"]
    males = data["male"]

    for female in females:
        new_data[female] = "female"

    for male in males:
        new_data[male] = "male"

    with open(filename + ".json", "w") as f:
        json.dump(new_data, f)


def get_new_column(filename):
    gender = []
    with open('names.json', 'r') as json_file:
        names_data = json.load(json_file)
    with open("./Data/"+filename + ".csv") as csvfile:
        csvreader = csv.reader(csvfile)
        i = -1
        for row in csvreader:
            i += 1
            if (i == 0):
                i += 1
                continue
            names = row[1].split()
            for name in names:
                if name.capitalize() in names_data:
                    gender.append(names_data[name.capitalize()])
                    break
                else:
                    gender.append("uknown")
                    break

    return gender


def add_column(filename, column_name):
    new_column_data = get_new_column("apple")
    print(new_column_data)
    df = pd.read_csv("./Data/"+filename+'.csv')
    df[column_name] = new_column_data
    df.to_csv(filename+'.csv', index=False)


# to_csv("ass_users")
# reformat_json("old_names")
# add_column("apple", "gender")
