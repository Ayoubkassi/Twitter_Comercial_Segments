from bs4 import BeautifulSoup
from get_gender import getNames
import json
import os

data = getNames()

with open("names.json", "w") as f:
    json.dump(data, f)
