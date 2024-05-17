#!/usr/bin/env python3
""" Program for parsing stock twitter account """

from sys import argv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import validators
from datetime import datetime, timedelta
import pytz


def main(file_path, ticker, time_interval) -> None:
    """
    The main function to run the programm

    :param file_path: The path to the file containing list of account links
    :param ticker: The string to search for
    :param time_interval: The time interval to search for occurrences of the ticker
    :return: None
    """
    print("\n Hello in the Stock Scrapper\n")

    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # Add this for WSL compatibility
    browser = webdriver.Chrome(options=chrome_options)

    # To avoid bot detection, for details: https://stackoverflow.com/a/75776883/22233201
    browser.execute_cdp_cmd("Page.removeScriptToEvaluateOnNewDocument", {"identifier": "1"})

    account_links = extract_urls_from_file(file_path)
    
    responses = [process_account_link(browser, account_link, ticker, time_interval) for account_link in account_links]
    print("resposes list: ", responses)
    num_list = [x for x in responses if x != None]
    browser.quit()
    print("#" * 30, "\n\n")
    print(f"{ticker} was mintioned {sum(num_list)} times in the last {time_interval} hours.\n")

def extract_urls_from_file(file):
    """
    Reads a file line by line, extracts URLs, and returns a list of URLs.
    :param file: The file path to read URLs from
    :return: A list of URLs extracted from the file
    """
    with open(file) as f:
        accounts_list = []
        for line in f:
            link = line.rstrip()
            if validators.url(link):
                accounts_list.append(link)
    return accounts_list

def process_account_link(browser, account_link , ticker, time_interval):
    """
    Process an individual account link asynchronously
    """
    try:
        print(f"\n\nProcessing account link: {account_link}")
        browser.get(account_link)
        tweets = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
        print("num of tweets found: ", len(tweets))
        count = 0
        for tweet in tweets:
            try:
                tweet_time_element = tweet.find_element(By.XPATH, ".//time").get_attribute("datetime")
                tweet_time = datetime.strptime(tweet_time_element, "%Y-%m-%dT%H:%M:%S.%fZ")
                now_time = datetime.now(pytz.utc).replace(tzinfo=None)
                if ((now_time - tweet_time) < time_interval):
                    count += tweet.text.count(ticker)
            except StaleElementReferenceException:
                print("Stale element reference exception, moving to next tweet.")
        print(f"Found {count} ticker.")
        return count
    except TimeoutException:
        print("Timed out waiting for page to load")
    except Exception as e:
        print("An error occurred while processing account link", e)

if __name__ == "__main__":
    time_units = {
        "mins": timedelta(minutes=1),
        "hours": timedelta(hours=1),
        "days": timedelta(days=1),
        "weeks": timedelta(weeks=1),
    }
    try:
        file_path = argv[1]
        ticker = argv[2]
        time_unit = argv[4]
        time_interval = time_units[time_unit] * int(argv[3])
        main(file_path, ticker, time_interval)
    except Exception:
        print("Usage: python3 test.py accounts.txt Ticker time_interval mins/hours/days/weeks")
        print("where:\n\ttime_interval is an integer")
        print("\ttime_unit is one of: mins, hours, days, weeks")
        print("\tTicker is a string to search for")
        print("\taccounts.txt is a path to a file containing list of twitter account links")
        print("\nExample: python3 test.py accounts.txt TSLA 24 hours\n")
