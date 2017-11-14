import json

with open('config.json') as data:
		config = json.load(data)

USER_REGION = config['Default']['Region']
KEY_PATH = config["Default"]["KeyPath"]