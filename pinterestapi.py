import httpx
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from urllib.parse import urljoin
import base64
from converter import *
import time
import json

load_dotenv()

@dataclass
class PinterestApi:
	base_api: str = 'https://api.pinterest.com'
	sandbox_base_api: str = 'https://api-sandbox.pinterest.com'
	client_id: str = None
	client_secret: str = None
	access_token: str = None
	authorization_code: str = None
	redirect_uri: str = None
	scopes: str = 'boards:read,boards:write,pins:read,pins:write'

	# Oauth
	def get_auth_url(self):
		print("Generating Authorization URL")
		auth_url = (
			f"https://www.pinterest.com/oauth/?response_type=code"
			f"&client_id={self.client_id}"
			f"&redirect_uri={self.redirect_uri}"
			f"&scope={self.scopes}"
		)
		print(f"Authorization URL: {auth_url}")

		return auth_url

	def get_access_token(self, grant_type='client_credentials'):
		endpoint = urljoin(self.base_api, '/v5/oauth/token')
		auth_string = f"{self.client_id}:{self.client_secret}"
		auth_base64 = base64.b64encode(auth_string.encode()).decode()

		headers = {
			"Authorization": f"Basic {auth_base64}",
			"Content-Type": "application/x-www-form-urlencoded"
		}

		if grant_type == 'client_credentials':
			data = {
				"grant_type": "client_credentials",
				"scope": "boards:read,boards:write,pins:read,pins:write"
			}
		elif grant_type == 'authorization_code':
			data = {
				"grant_type": "authorization_code",
				"code": self.authorization_code,
				"redirect_uri": self.redirect_uri,
				"scope": "boards:read,boards:write,pins:read,pins:write"
			}

		with httpx.Client(headers=headers) as client:
			response = client.post(endpoint, data=data)

			if response.status_code == 200:
				data = response.json()
				self.access_token = data.get("access_token")
				with open('access_token.json', "w") as file:
					json.dump({"access_token": self.access_token}, file)

			else:
				print("Error:", response.status_code, response.text)

				return None

	def retriev_access_token(self):
		with open('access_token.json', "r") as file:
			data = json.load(file)
			retrieved_token = data.get("access_token")

		return retrieved_token

	# Create
	def create_pin(self, payload):
		endpoint = urljoin(self.base_api, '/v5/pins')

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		error_count = 0
		while error_count < 3:
			with httpx.Client(headers=headers) as client:
				response = client.post(endpoint, json=payload)

				if response.status_code == 200 or response.status_code == 201:
					print("Succeed:", response.status_code, response.text)
					error_count = 0
					return response
				else:
					print("Resize image:", response.status_code, response.text)
					time.sleep(3)
					payload = resize_image(payload)
					error_count += 1
		if error_count >= 3:
			print("Error:", response.status_code, response.text)
			return response

	def get_upload_url(self, media_type):
		endpoint = urljoin(self.base_api, '/v5/media')

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		payload = {
			"media_type": media_type
		}

		with httpx.Client(headers=headers) as client:
			response = client.post(endpoint, json=payload)

			if response.status_code == 201:
				return response.json()

			else:
				print("Error:", response.status_code, response.text)
				return response

	def upload_video(self, video_url):
		headers = {
			"Authorization": f"Bearer {access_token}"
		}

		files = {
			"media": open(video_file_path, "rb")
		}

		response = requests.post(upload_url, headers=headers, files=files)
		if response.status_code != 201:
			return {"error": f"Video upload failed: {response.text}"}

		upload_response = response.json()
		media_id = upload_response.get("id")  # Media ID for the uploaded video

		if not media_id:
			return {"error": "Media ID not received from Pinterest"}

	# Read
	def list_pins(self, params=None):
		endpoint = urljoin(self.base_api, '/v5/pins')

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		with httpx.Client(headers=headers) as client:
			response = client.get(endpoint, params=params)

			if response.status_code == 200:
				data = response.json()
				print(data)

			else:
				print("Error:", response.status_code, response.text)

	def list_boards(self, params):
		endpoint = urljoin(self.base_api, '/v5/boards')

		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		with httpx.Client(headers=headers) as client:
			response = client.get(endpoint, params=params)

			if response.status_code == 200:
				return response
				print("Succeed:", response.status_code, response.text)

			else:
				print("Error:", response.status_code, response.text)

	# Update

	# Delete


if __name__ == '__main__':
	app = PinterestApi(
		client_id=os.getenv('PINTEREST_APP_ID'),
		client_secret=os.getenv('PINTEREST_SECRET_KEY'),
		redirect_uri=os.getenv('REDIRECT_URI'),
		# authorization_code='79fcb1e3b8ea006fd780f734e49100af7cd731a3'
	)

	app.get_access_token(grant_type='client_credentials')

	params = {
		"page_size": 100
	}

	# print(app.access_token)

	# app.list_pins(params=params)

	app.list_boards(params=params)

	# payload = {
	# 	"link": "https://www.magiccars.com/products/ride-on-car-covers-a-shield-against-rain-sun-dust-snow-and-leaves",
	# 	"title": "12V Aqua Marina Electric Pump (16 psi)",
	# 	"description": "12V Electric Pump Specifications: 12V DC electric pump up to 16psi, 110W Inflates: iSUP boards, kayaks, boats and air platforms LCD screen Cigarette lighter or battery attachable Inflate: 70L/min.",
	# 	"dominant_color": "#6E7874",
	# 	"alt_text": "alt_text",
	# 	"board_id": "1089026822333747466",
	# 	# "board_section_id": "string",
	# 	"media_source": {
	# 		"source_type": "image_url",
	# 		"url": "https://cdn.shopify.com/s/files/1/2245/9711/files/12V_Aqua_Marina_Electric_Pump_16_psi_-_DTI_Direct_USA-2597608.png",
	# 		"is_standard": True
	# 	}
		# "parent_pin_id": "string",
		# "note": "string",
		# "sponsor_id": "string"
	# }

	# app.create_pin(payload=payload)

	# app.get_upload_url(media_type="video")
