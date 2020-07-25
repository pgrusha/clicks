import requests
import os
import sys
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

def create_parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url')
    return parser


def shorten_link(token, url):
    headers = {'Authorization':'Bearer {}'.format(token)}
    payload = {'long_url': url}
    service_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(service_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def is_short_link(token, url):
    sep_url = urlparse(url)
    headers = {'Authorization':'Bearer {}'.format(token)}
    payload = {'bitlink_id': url[len(sep_url[0]) + 3:]}
    service_url = 'https://api-ssl.bitly.com/v4/expand'
    response = requests.post(service_url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return False
    return True


def count_clicks(token, link):
    sep_url = urlparse(link)
    headers = {'Authorization':'Bearer {}'.format(token)}
    service_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/{}/clicks/summary'.format(sep_url[1], sep_url[2])
    response = requests.get(service_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parser = create_parser()
    cline_params = parser.parse_args()
    if is_short_link(token, cline_params.url):
        try:
            success = True
            clicks_count = count_clicks(token, cline_params.url)
        except requests.exceptions.HTTPError:
            success = False
            print('Сервер вернул ошибку. Возможно, адрес неверный')
        if success:
            print('Количество кликов', clicks_count)
    else:
        try:
            bitlink = shorten_link(token, cline_params.url)
        except requests.exceptions.HTTPError:
            bitlink = None
            print('Сервер вернул ошибку. Возможно, адрес неверный')
        if bitlink:
            print('Битлинк', bitlink)
