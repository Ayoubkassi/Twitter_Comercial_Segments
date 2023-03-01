import requests
from bs4 import BeautifulSoup


def getNames():
    # different genders and their corresponding number of pages
    genders = {"female": ["feminine", 41], "male": ["masculine", 50]}
    data = {}
    for key, val in genders.items():
        my_names = []
        for i in range(1, val[1]):
            url = "https://www.behindthename.com/names/gender/" + val[0] + "/" + str(i)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            names = soup.find_all("a", {"class": "nll"})
            my_names.extend([name.text for name in names])
        data[key] = my_names
    return data
