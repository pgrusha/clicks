import requests
import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url', nargs='?')
    return parser


def shorten_link(token, url):
    headers = {'Authorization':'Bearer {}'.format(token)}
    payload = {'long_url': url}
    service_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(service_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    if link.startswith('https://'):
        link = link[8:]
    elif link.startswith('http://'):
        link = link[7:]
    headers = {'Authorization':'Bearer {}'.format(token)}
    service_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(link)
    response = requests.get(service_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


if __name__ == '__main__':
    token = os.getenv("BITLY_TOKEN")
#    print('Введите ссылку')
#    url = input()
    parser = createParser()
    namespace = parser.parse_args()
    if (namespace.url.startswith('https://bit.ly/')):
        try:
            clicks_count = count_clicks(token, namespace.url)
        except requests.exceptions.HTTPError:
            clicks_count = None
            print('Сервер вернул ошибку. Возможно, адрес неверный')
        if clicks_count:
            print('Количество кликов', clicks_count)
    else:
        try:
            bitlink = shorten_link(token, namespace.url)
        except requests.exceptions.HTTPError:
            bitlink = None
            print('Сервер вернул ошибку. Возможно, адрес неверный')
        if bitlink:
            print('Битлинк', bitlink)
