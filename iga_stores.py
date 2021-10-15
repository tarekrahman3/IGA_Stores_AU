import requests
import json
import re
import pandas as pd

base = 'https://embed.salefinder.com.au/location/search/183/?query='
data_bucket = []

def generate_url(zip_code):
	return base+str(zip_code)

def send_request(url):
	return requests.get(url)

def trim_response(resp):
	return re.sub(r'^\(|\)$','',resp.text)

def convert_to_dictionary(text):
	return json.loads(text)

def check_result_length(dictionary):
	return len(dictionary['result'])

def store_data(zip_code, dictionary, bucket):
	for i in range(len(dictionary['result'])):
		#print({**{'zip_code':zip_code}, **dictionary['result'][i]})
		bucket.append({**{'zip_code':zip_code}, **dictionary['result'][i]})

def main_sequence(zip_code):
	url = generate_url(zip_code)
	resp = send_request(url)
	text = trim_response(resp)
	dictionary = convert_to_dictionary(text)
	length = check_result_length(dictionary)
	if length>0:
		store_data(zip_code, dictionary, data_bucket)

zip_codes = pd.read_csv('import.csv').codes.tolist()

try:
	for index, zip_code in enumerate(zip_codes):
		main_sequence(zip_code)
		print(f"{index} | {zip_code}")

finally:
	pd.DataFrame(data_bucket).to_csv('data.csv',index=False)
