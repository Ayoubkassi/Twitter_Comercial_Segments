import json
import csv


def to_csv(filename):
    with open("../data/"+ filename + '.json', 'r') as json_file:
        data = json.load(json_file)

    with open("../data/" + filename+'.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(data[0].keys())

        for row in data:
            writer.writerow(row.values())



# we changed the scrapped names data to a hashmap to make the complexity of the code constant and not linear as it was.
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


to_csv("apple_users")
# reformat_json("old_names")
