import pandas as pd
import ast
import re


def to_payload(df_row):
    payload = dict()
    payload['link'] = df_row['Link']
    if len(df_row['Title']) > 99:
        payload['title'] = df_row['Title'][0:99]
    else:
        payload['title'] = df_row['Title']
    if len(df_row['Description']) > 799:
        payload['description'] = df_row['Description'][0:799]
    else:
        payload['description'] = df_row['Description']
    payload['board_id'] = '1089026822333747466'
    payload['media_source'] = dict()
    items = list()
    media_url_list = ast.literal_eval(df_row['Media URL'])
    # media_thumbnail_list = df['Thumbnail']
    if len(media_url_list) > 1:
        payload['media_source']['source_type'] = 'multiple_image_urls'
        if len(media_url_list) < 5:
            for i in range(len(media_url_list)):
                item = {
                    # 'source_type': 'image_base_64',
                    # 'title': payload['title'],
                    # 'description': payload['description'],
                    # 'link': payload['link'],
                    'url': media_url_list[i] + '&width=1200&height=1200&crop=center'
                }
                items.append(item)
        else:
            for i in range(5):
                item = {
                    # 'source_type': 'image_base_64',
                    # 'title': payload['title'],
                    # 'description': payload['description'],
                    # 'link': payload['link'],
                    'url': media_url_list[i] + '&width=1200&height=1200&crop=center'
                }
                items.append(item)
        payload['media_source']['items'] = items
    else:
        payload['media_source']['source_type'] = 'image_url'
        payload['media_source']['url'] = media_url_list[0] + '&width=1200&height=1200&crop=center'
        payload['media_source']['is_standard'] = False

    return payload


def resize_image(payload):
    if payload['media_source']['source_type'] == 'multiple_image_urls':
        new_items = list()
        for item in payload['media_source']['items']:
            matches = re.search(r'width=(\d+)&height=(\d+)', item['url'])
            width = matches.group(1)
            height = matches.group(2)
            if width == '1200':
                url_modified = re.sub(r'width=\d+', 'width=900', item['url'])
                url_modified = re.sub(r'height=\d+', 'height=900', url_modified)
            elif width == '900':
                url_modified = re.sub(r'width=\d+', 'width=600', item['url'])
                url_modified = re.sub(r'height=\d+', 'height=600', url_modified)
            elif width == '600':
                url_modified = re.sub(r'width=\d+', 'width=300', item['url'])
                url_modified = re.sub(r'height=\d+', 'height=300', url_modified)
            elif width == '300':
                url_modified = re.sub(r'width=\d+', 'width=150', item['url'])
                url_modified = re.sub(r'height=\d+', 'height=150', url_modified)
            new_items.append({'url': url_modified})
        payload['media_source']['items'] = new_items
        print(payload)

    else:
        matches = re.search(r'width=(\d+)&height=(\d+)', payload['media_source']['url'])
        width = matches.group(1)
        height = matches.group(2)
        payload['media_source']['url']
        if width == '1200':
            url_modified = re.sub(r'width=\d+', 'width=900', payload['media_source']['url'])
            url_modified = re.sub(r'height=\d+', 'height=900', url_modified)
        elif width == '900':
            url_modified = re.sub(r'width=\d+', 'width=600', payload['media_source']['url'])
            url_modified = re.sub(r'height=\d+', 'height=600', url_modified)
        elif width == '600':
            url_modified = re.sub(r'width=\d+', 'width=300', payload['media_source']['url'])
            url_modified = re.sub(r'height=\d+', 'height=300', url_modified)
        elif width == '300':
            url_modified = re.sub(r'width=\d+', 'width=150', payload['media_source']['url'])
            url_modified = re.sub(r'height=\d+', 'height=150', url_modified)
        payload['media_source']['url'] = url_modified
        print(payload)

    return payload

if __name__ == '__main__':
    df = pd.read_csv('data/grouped_data.csv')
    payload = {
        "link": "https://www.magiccars.com/products/ride-on-car-covers-a-shield-against-rain-sun-dust-snow-and-leaves",
        "title": "12V Aqua Marina Electric Pump (16 psi)",
        "description": "12V Electric Pump Specifications: 12V DC electric pump up to 16psi, 110W Inflates: iSUP boards, kayaks, boats and air platforms LCD screen Cigarette lighter or battery attachable Inflate: 70L/min.",
        # "dominant_color": "#6E7874",
        # "alt_text": "alt_text",
        "board_id": "1089026822333747466",
        # "board_section_id": "string",
        "media_source": {
            "source_type": "image_url",
            "url": "https://cdn.shopify.com/s/files/1/2245/9711/files/12V_Aqua_Marina_Electric_Pump_16_psi_-_DTI_Direct_USA-2597608.png",
            "is_standard": True
        }
    }
    payloads = df.apply(to_payload, axis=1)
