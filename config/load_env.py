import os

def load_env():
	with open(".env", "r") as f:
		data_text = f.read()
		data_list = data_text.split("\n")
		for data in data_list:
			key,value = data.split("=")
			os.environ[key] = value