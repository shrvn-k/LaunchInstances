import json
import os

os.chdir(os.path.dirname(__file__))
with open('config.json') as data:
		config = json.load(data)

USER_REGION = config['Default']['Region']
KEY_PATH = config["Default"]["KeyPath"]
