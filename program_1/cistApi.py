import requests
import time
import os

class CISTApi:
	def __init__(self):
		self.url= os.environ.get('API_URL')
		self.auth_token = ""

		self.getRegisterToken()

	# Function to get authentication token
	def getRegisterToken(self):
		r = requests.get(f"{self.url}/register")
		data = r.json()

		if "status" in data and data["status"] == 200:
			self.auth_token = data["data"]['authorizationToken']
		else:
			print("[!] Failed to request Register API. Reason: ", data["message"])
	
	# Function to get data file url
	# API max retry will be 5
	# If hit rate limit erro, wait another 3 second and try again
	def postRequestFileUrl(self, next_id = "", tried = 0):
		header= {"authorizationToken": self.auth_token}
		payload = {"next_id": next_id}
		r = requests.post(f"{self.url}/download-dataset",headers=header, json=payload)
		data = r.json()

		dataset_data = (None, None)
		if "status" in data:
			if data["status"] == 200:
				dataset_data= (data["data"]["dataset_url"], data["data"]["next_id"])
			elif data["status"] == 429 and tried < 5:
				# API max retry will be 5
				# If hit rate limit erro, wait another 3 second and try again
				print("[!] Failed to get data file url, tried: ", tried + 1)
				time.sleep(3)
				dataset_data = self.postRequestFileUrl(next_id, tried + 1)
			else:
				print(f"[!] Failed to request Download Dataset API. Reason: {data['status']}-{data['message']}")
		else:
			print("[!] Failed to request Download Dataset API. Reason: ", data["message"])

		return dataset_data

