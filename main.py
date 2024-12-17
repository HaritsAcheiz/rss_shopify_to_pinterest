# from shopifyapi import ShopifyApp
from pinterestapi import PinterestApi
from converter import *

from dotenv import load_dotenv
import os
from flask import Flask, request, redirect, render_template, session, url_for
import pandas as pd

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

pinapp = PinterestApi(
    client_id=os.getenv('PINTEREST_APP_ID'),
    client_secret=os.getenv('PINTEREST_SECRET_KEY'),
    redirect_uri=os.getenv('REDIRECT_URI')
)


@app.route("/")
def index():
    """Render the home page with instructions."""
    access_granted = session.get("access_granted", False)
    return render_template("index.html", access_granted=access_granted)


@app.route("/upload_video")
def upload_video():
    """Endpoint placeholder for uploading a video."""
    return "Feature to upload a video coming soon!"


@app.route("/start_pinterest_auth")
def start_pinterest_auth():
    """Redirect the user to Pinterest's OAuth page."""
    auth_url = pinapp.get_auth_url()
    return redirect(auth_url)


# @app.route("/pinterest_redirect")
# def pinterest_redirect():
#     pinapp.authorization_code = request.args.get("code")
#     if not pinapp.authorization_code:
#         return "Error: No authorization code received."
#     pinapp.get_access_token(grant_type='authorization_code')
#     print("Access Granted!!!")

#     return redirect("/")

@app.route("/pinterest_redirect")
def pinterest_redirect():
    """Handle Pinterest redirect and set access granted."""
    pinapp.authorization_code = request.args.get("code")
    if not pinapp.authorization_code:
        return "Error: No authorization code received."

    try:
        # Get access token
        pinapp.get_access_token(grant_type='authorization_code')
        session["access_granted"] = True
        print("Access Granted!!!")
        return redirect(url_for("index"))  # Redirect to index page
    except Exception as e:
        return f"Error during authorization: {str(e)}"


# @app.route("/create_pin")
# def create_pin():
#     df = pd.read_csv('data/grouped_data.csv')
#     sample_df = df[30:41]
#     payloads = sample_df.apply(to_payload, axis=1).to_list()

#     # for payload in payloads:
#     pinapp.create_pin(payload=payloads[0])

#     return

@app.route("/create_pin")
def create_pin():
    """Create Pinterest pins from a sample CSV file."""
    if not session.get("access_granted"):
        return redirect(url_for("start_pinterest_auth"))

    try:
        # Read CSV and prepare payloads
        df = pd.read_csv("data/grouped_data.csv")
        sample_df = df[30:41]  # Select rows to process
        payloads = sample_df.apply(to_payload, axis=1).to_list()

        # Create pins and log success
        success_count = 0
        for payload in payloads:
            response = pinapp.create_pin(payload=payload)
            if response.status_code == 201:  # Check for successful creation
                success_count += 1

        return f"Successfully created {success_count} pins!"
    except Exception as e:
        return f"Error while creating pins: {str(e)}"


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)

    # base_url = 'https://www.magiccars.com/products'
    # s = ShopifyApp(
    #     store_name=os.getenv('STORE_NAME'),
    #     access_token=os.getenv('SHOPIFY_ACCESS_TOKEN'),
    #     version='2024-10'
    # )

    # client = s.create_session()
    # has_next_page = True
    # cursor = None
    # results = list()
    # counter = 1
    # while has_next_page:
    #     print('Page {}'.format(counter))
    #     while 1:
    #         try:
    #             response = s.query_products(client, cursor=cursor)
    #             records = response['data']['products']['edges']
    #             break
    #         except Exception as e:
    #             print(e)
    #             print(response)
    #             sleep(5)
    #             continue
    #     for record in records:
    #         media_records = record['node']['media']['edges']
    #         for media_record in media_records:
    #             try:
    #                 data = dict()
    #                 data['Title'] = record['node']['title']
    #                 data['Pinterest board'] = 'magic_cars_ride_on_toys'
    #                 try:
    #                     data['Media URL'] = media_record['node']['originalSource']['url'] if media_record['node']['mediaContentType'] == 'VIDEO' else media_record['node']['preview']['image']['url']
    #                 except Exception as e:
    #                     data['Media URL'] = media_record['node']['preview']['image']['url']
    #                 try:
    #                     data['Thumbnail'] = 0.02 if media_record['node']['mediaContentType'] == 'VIDEO' else ''
    #                 except Exception as e:
    #                     data['Thumbnail'] = ''
    #                 data['Description'] = record['node']['seo']['description'] if (record['node']['seo']['description'] != '') and (record['node']['seo']['description'] is not None) else record['node']['description']
    #                 data['Link'] = record['node']['onlineStoreUrl']
    #                 data['Publish date'] = ''
    #                 data['Keywords'] = ','.join(record['node']['tags']).lower()
    #                 results.append(data.copy())
    #             except Exception as e:
    #                 print(media_record['node'])
    #                 pass
    #     has_next_page = response['data']['products']['pageInfo']['hasNextPage']
    #     cursor = response['data']['products']['pageInfo']['endCursor']
    #     counter += 1

    # results_df = pd.DataFrame.from_records(results)
    # results_df.to_csv('data/products.csv', index=False)

    # df = pd.read_csv('data/products.csv')
    # df = df[pd.notna(df['Link'])]
    # df.fillna('', inplace=True)
    # grouped_df = df.groupby(['Title', 'Pinterest board', 'Description', 'Link', 'Publish date', 'Keywords']).agg(list).reset_index()
    # grouped_df.to_csv('data/grouped_data.csv', index=False)
    # df = make_titles_unique(df)
    # chunk_dataframe(df)

    # df = pd.read_csv('data/grouped_data.csv')
    # sample_df = df[30:41]
    # payloads = sample_df.apply(to_payload, axis=1).to_list()

    # app = PinterestApi(client_id=os.getenv('PINTEREST_APP_ID_P'), client_secret=os.getenv('PINTEREST_SECRET_KEY_P'))
    # app.get_access_token()

    # params = {
    #     "page_size": 100
    # }

    # # for payload in payloads:
    # app.create_pin(payload=payloads[0])

    # app.list_pins()

    # app.list_boards(params=params)