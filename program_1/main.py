import concurrent.futures
import json
import re
import requests
import os
import time

from cistApi import CISTApi

SANITIZED_DATASET = []

def data_validate(data):
	name_regex_pattern = r"^[a-zA-z ]+$"
	rating_regex = lambda x: x != None and (1.00 <= x <= 10.00)
	distance_regex = lambda x: x != None and (10.00 <= x <= 1000.00)

	name_regex = re.compile(name_regex_pattern)
	name_regex_result = name_regex.match(data['restaurant_name'])

	if name_regex_result != None and rating_regex(data["rating"]) and distance_regex(data["distance_from_me"]):
		return True
	else:
		return False

def data_sanitization(file_url, thread_id):
	try:
		r = requests.get(file_url)
		dataset = r.json()

		for data in dataset:
			if data_validate(data):
				SANITIZED_DATASET.append(data)
		print(f"[#] Data sanitization thread {thread_id} finished.")
	except Exception as e:
		print("[!] Error on data sanitization: ", e)

	print()

def main():
	# Initial thread pool
	pool = concurrent.futures.ThreadPoolExecutor(max_workers=4)

	cisp_api = CISTApi()

	data_next_id=""
	thread_id = 1
	while True:
		print("[#] Requesting the data file, next_id: ", data_next_id)
		file_url, data_next_id = cisp_api.postRequestFileUrl(data_next_id)
		if file_url != None:
			pool.submit(data_sanitization, file_url, thread_id)
			thread_id += 1
			if data_next_id != "":
				# Wait 12 second for to get next data set
				print("[#] Pause 12 second to avoid request blocked by rate limit.")
				time.sleep(12)
			else:
				break
		else:
			print("[!] Error in API request.")
			break

	pool.shutdown(wait=True)

	if len(SANITIZED_DATASET) > 0:
		print("[#] Creating Json file...")
		# Serializing json
		json_object = json.dumps(SANITIZED_DATASET, indent=4)

		# Write data into json file
		with open("validated_dataset.json", "w+") as outfile:
			outfile.write(json_object)
		print("[#] Json file created.")
	else:
		print("[!] Empty data set!")

	# Verify the dataset
	print()
	print("[#] Verify sanitized dataset")
	url = os.environ.get('API_URL')
	r = requests.post(f"{url}/test/check-data-validation", json={ "data": SANITIZED_DATASET })
	print(r.json())

main()
