import requests
import schedule
import re
import time
from flask import jsonify
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date

def main():

#     current_date = datetime.date.today()
    # Test - 3. april 2024.
    current_date = datetime(2024, 4, 3)

    next_day = current_date + timedelta(days=1)

    date = get_current_date(next_day)
    month = get_current_month(next_day)
    day = get_current_day(next_day)

    # +1 because we look for dates in the future
    formatted_date = f'{date}-{month}'

    url_base = 'https://subotica.com/vesti'

    # Define a regular expression pattern to match URLs
    url_pattern = f'{url_base}/iskljucenja-struje-za-{formatted_date}-{day}-id*'

    urls = find_valid_urls(url_base, url_pattern)

    if urls:
        for url in urls:
            print(url)
            status = check_for_string(url)
            if (status):
                webhook("Nema iskljucenja danas")
            else:
                print("Nema iskljucenja danas. :)")
                webhook(url)
    else:
        webhook("Nema iskljucenja danas")
        print("Nema iskljucenja danas :)")


def webhook(message):
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = 'AIzaSyAmweWxrVGyBozSYPtrZ2UT5gfrl6x_xMw'
    chat_group = "AAAAFUb0EFI"

    # Construct message payload for Google Chat API
    payload = {
        'text': message,
        'thread': {'name': chat_group}
    }

    url = f'https://chat.googleapis.com/v1/spaces/{chat_group}/messages?key={api_key}'

    # Send message to Google Chat
    response = requests.post(url, json=payload)

    if response.ok:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': response.text}), 500


def find_valid_urls(base_url, pattern):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    valid_urls = []

    for link in links:
        url = link['href']
        if re.match(pattern, url):
            valid_urls.append(url)

    return valid_urls


def check_for_string(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the <div> element with class "article__text plain-text"
        article_text_div = soup.find('div', class_='article__text plain-text')

        # Check if the element is found and if "Somborski put" is in its text
        if article_text_div and "Somborski put" in article_text_div.get_text():
            return True

    # Return False if the string is not found or there was an error
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
#     app.run(debug=True)

# Schedule the task to run at noon every day
# schedule.every().day.at('12:00').do(main)

# # Run the scheduler continuously
# while True:
#     schedule.run_pending()
#     time.sleep(1)  # Optional: Add a small delay to avoid high CPU usage
