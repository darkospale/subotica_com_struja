import requests
import schedule
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from chat_create_text_message_app import webhook

def main():
    current_date = datetime.today()

    next_day = current_date + timedelta(days=1)

    date = get_current_date(next_day)
    month = get_current_month(next_day)
    day = get_current_day(next_day)

    # +1 because we look for dates in the future
    formatted_date = f'{date}-{month}'

    url_base = 'https://www.subotica.com/vesti'

    # Define a regular expression pattern to match URLs
    url_pattern = f'{url_base}/iskljucenja-struje-za-{formatted_date}-{day}-id'

    urls = find_valid_urls(url_base, url_pattern)

    if urls:
        for url in urls:
            status = check_for_string(url)
            if (status):
                webhook(url)
            else:
                webhook("Nema iskljucenja danas. :)")
    else:
        webhook("Nema iskljucenja danas")


def find_valid_urls(url_base, pattern):
    grab = requests.get(url_base)
    soup = BeautifulSoup(grab.text, 'html.parser')

    f = open("webpages.txt", "w")
    for link in soup.find_all("a"):
       data = link.get('href')
       f.write(data)
       f.write("\n")

    valid_urls = []
    with open("webpages.txt", "r") as file:
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

        if article_text_div and "Somborski put" in article_text_div.get_text():
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


if __name__ == "__main__":
    main()


# Schedule the task to run at noon every day
# schedule.every().day.at('12:00').do(main)