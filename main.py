import httpx
from pinterestapi import PinterestApi
import os
from dotenv import load_dotenv
import pandas as pd
from converter import *
import time

load_dotenv()


if __name__ == '__main__':

	pinapp = PinterestApi(
		client_id=os.getenv('PINTEREST_APP_ID'),
		client_secret=os.getenv('PINTEREST_SECRET_KEY'),
		redirect_uri=os.getenv('REDIRECT_URI')
	)

	pinapp.access_token = pinapp.retriev_access_token()

	# params = {
	# 	"page_size": 100
	# }
	# response = pinapp.list_boards(params=params)
	# print(response.headers)

	# df = pd.read_csv('data/products.csv')
	# video_df = df[~df['Thumbnail'].isnull()]

	# group_data('data/products.csv')

	# df = pd.read_csv("data/grouped_data.csv")
	# chunk_dataframe(df)

	filepath = "chunked_data/chunk_18.csv"
	df = pd.read_csv(filepath)

	if 'is_imported' not in df.columns:
		df['is_imported'] = False
	else:
		df = df[~df['is_imported']].reset_index(drop=True)

	df.fillna('', inplace=True)
	payloads = df.apply(to_payload, axis=1).to_list()

	success_count = 0
	try:
		for index, payload in enumerate(payloads):
			time.sleep(3)
			try:
				response = pinapp.create_pin(payload=payload)
				if response.status_code == 201:  # Check for successful creation
					success_count += 1
					df.at[index, 'is_imported'] = True  # Mark as imported
				headers = response.headers
				if int(headers.get('x-ratelimit-remaining')) <= 10:
					time.sleep(90)
			except Exception as pin_error:
				print(f"Error while creating pin for row {index}: {str(pin_error)}")

	except Exception as e:
		print(f"Error while processing payloads: {str(e)}")
	finally:
		df.to_csv(filepath, index=False)
		print(f"Successfully created {success_count} pins and updated the file!")
