from datetime import datetime as dt

import requests
from django.http import HttpRequest, HttpResponse

from .models import Letters


# Create your views here.
def download_json() -> list:
    url = f'https://hubofdata.ru/storage/f/2013-08-18T19%3A58%3A51.196Z/greetings-data.json'
    month_values = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }
    try:
        with requests.Session() as session:
            response = session.get(url)
    except Exception as exc:
        print(exc)
    else:
        if response.status_code == 200:
            print('Success downloading data from given URL!')
            response = response.json()
            for dict_row in response['items']:
                date_list = dict_row['thedate'].split(sep=' ')[:3]
                for k, v in month_values.items():
                    date_list[1] = date_list[1].replace(k, v)
                dict_row['thedate'] = dt.strptime(f'{date_list[0]} {date_list[1]} '
                                                  f'{date_list[2]}', '%d %m %Y').date()
            return response['items']

        elif response.status_code == 404:
            print('Not Found data from given URL')


def save_to_model(request: HttpRequest) -> HttpResponse:
    # TODO: Async connection to DataBase
    processed_list = download_json()
    if processed_list:
        for dict_row in processed_list:
            if not Letters.objects.get(id=int(dict_row['id'])):
                greetings = Letters(id=int(dict_row['id']),
                                    category=dict_row['category'],
                                    sender=dict_row['from'],
                                    title=dict_row['title'],
                                    text=dict_row['text'],
                                    date=dict_row['thedate'],
                                    )
                greetings.save()
        print('All greetings are saved in Django Model')
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
