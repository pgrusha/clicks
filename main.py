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
    scheme, *_ = urlparse(url)
    headers = {'Authorization':'Bearer {}'.format(token)}
    payload = {'bitlink_id': url[len(scheme) + 3:]}
    service_url = 'https://api-ssl.bitly.com/v4/expand'
    response = requests.post(service_url, headers=headers, json=payload)
    return response.ok


def count_clicks(token, link):
    _, netloc, path, *_ = urlparse(link)
    headers = {'Authorization':'Bearer {}'.format(token)}
    service_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/{}/clicks/summary'.format(netloc, path)
    response = requests.get(service_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parser = create_parser()
    namespace = parser.parse_args()
    if is_short_link(token, namespace.url):
        try:
            clicks_count = count_clicks(token, namespace.url)
            print('Количество кликов', clicks_count)
        except requests.exceptions.HTTPError:
            print('Сервер вернул ошибку. Возможно, адрес неверный')
    else:
        try:
            bitlink = shorten_link(token, namespace.url)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError:
            print('Сервер вернул ошибку. Возможно, адрес неверный')
