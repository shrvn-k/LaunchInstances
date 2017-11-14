import json
from pprint import pprint

data = open('config.json','r')
config = json.load(data)
region = "ap-south-1"
print config["EC2"]["Regions"][region]["KeyName"]
