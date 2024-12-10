from shopifyapi import ShopifyApp
from dotenv import load_dotenv
import os
import pandas as pd
from httpx import ReadTimeout
from time import sleep

load_dotenv()


def chunk_dataframe(df, chunk_size=200, output_dir='chunked_data', prefix='chunk_'):
    os.makedirs(output_dir, exist_ok=True)
    output_files = []
    num_chunks = (len(df) + chunk_size - 1) // chunk_size

    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(df))

        chunk = df.iloc[start_idx:end_idx]
        output_path = os.path.join(output_dir, f'{prefix}{i+1}.csv')

        chunk.to_csv(output_path, index=False)
        output_files.append(output_path)

        print(f'Saved {output_path}: {len(chunk)} rows')


def make_titles_unique(df, title_column='Title'):
    df_unique = df.copy()
    title_counts = {}

    # Function to generate unique title
    def get_unique_title(title):
        if title not in title_counts:
            # First occurrence of the title
            title_counts[title] = 0
            return title
        else:
            # Increment count for duplicate titles
            title_counts[title] += 1
            # Add sequence number to make it unique
            return f"{title} ({title_counts[title]})"

    # Apply unique title generation
    df_unique[title_column] = df_unique[title_column].apply(get_unique_title)

    return df_unique


if __name__ == '__main__':
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

    df = pd.read_csv('data/products.csv')
    df = df[pd.notna(df['Link'])]
    df = make_titles_unique(df)
    chunk_dataframe(df)