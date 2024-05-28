#!/usr/bin/python3

import requests
import schedule
import re
import time
import telebot
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
# from chat_create_text_message_app import webhook

def main():
    load_dotenv()

    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

    bot = telebot.TeleBot(TELEGRAM_API_KEY)

    # Test
    # current_date = datetime(2024, 4, 8)
    current_date = datetime.today()

    next_day = current_date + timedelta(days=1)

    date = get_current_date(next_day)
    month = get_current_month(next_day)
    day = get_current_day(next_day)

    if day == 'subota' or day == 'nedelja':
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Vikend je.')
        return

    default_msg = f'{current_date} - Nema iskljucenja za sutra.'

    # +1 because we look for dates in the future
    formatted_date = f'{date}-{month}'

    url_base = 'https://www.subotica.com/vesti'

    # Define a regular expression pattern to match URLs
    url_pattern = f'{url_base}/iskljucenja-struje-za-{formatted_date}-{day}-id'

    urls = find_valid_urls(url_base, url_pattern)

    # @todo Handle google chat webhook.
    if urls:
        for url in urls:
            status = check_for_string(url)
            if (status):
                message = f'Iskljucenje na adresi Somborski put sutra. Detaljnije info na linku: {url}'
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            else:
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=default_msg)
    else:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=default_msg)


def find_valid_urls(url_base, pattern):
    grab = requests.get(url_base)
    soup = BeautifulSoup(grab.text, 'html.parser')

    f = open("webpages", "w")
    for link in soup.find_all("a"):
       data = link.get('href')
       f.write(data)
       f.write("\n")

    valid_urls = []
    with open("webpages", "r") as file:
        for line in file:
            if re.match(pattern, line.strip()):
                valid_urls.append(line.strip())

    res = []
    [res.append(x) for x in valid_urls if x not in res]

    return res


def check_for_string(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        article_text_div = soup.find('div', class_='article__text plain-text')

        list = [
            'Somborski put između brojeva',
            'Somborski put 33a',
            'Somborski put'
        ]

        if article_text_div.get_text() in list:
            return True

    return False


def get_current_date(current_date):
    current_day = current_date.day

    return current_day


def get_current_month(current_date):
    # -1 because of key value.
    current_month = current_date.month-1

    months_of_week = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]
    current_month_str = months_of_week[current_month]

    return current_month_str


def get_current_day(current_date):
    current_day = current_date.weekday()

    # Get the current day (as a string)
    days_of_week = ["ponedeljak", "utorak", "sreda", "cetvrtak", "petak", "subota", "nedelja"]
    current_day_str = days_of_week[current_day]

    return current_day_str

# Test
# schedule.every(10).minutes.do(main)
# schedule.every().day.at("11:00", "Europe/Belgrade").do(main)

if __name__ == '__main__':
    main()

# while True:
#     schedule.run_pending()
#     time.sleep(10)
