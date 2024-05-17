# X_Scraper

## Description

The **X_Scraper** is a Python script that parses Twitter accounts to search for mentions of a specific stock ticker within a specified time interval. The script uses Selenium WebDriver to automate the browsing and extraction of tweets from the specified Twitter accounts. The primary use case is to determine how many times a particular stock ticker has been mentioned in tweets within the given time frame.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.6 or higher
- Selenium
- Google Chrome (for the WebDriver)
- ChromeDriver (compatible with your version of Google Chrome)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Mostafa1Jamal1/X_Scraper.git
   cd X_Scraper
   ```

2. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver:**

   Download the ChromeDriver from [here](https://sites.google.com/chromium.org/driver/downloads) and place it in your system's PATH or in the same directory as the script.

## Usage

To run the X_Scraper, use the following command:

```bash
python3 Stock_scraper.py accounts.txt Ticker time_interval time_unit
```

### Parameters

- `accounts.txt`: Path to the file containing the list of Twitter account links (one per line).
- `Ticker`: The stock ticker symbol to search for (e.g., TSLA).
- `time_interval`: An integer representing the amount of time to look back (e.g., 24).
- `time_unit`: The unit of time for the `time_interval`. Valid values are:
  - `mins`: Minutes
  - `hours`: Hours
  - `days`: Days
  - `weeks`: Weeks

### Example

To search for mentions of the stock ticker "TSLA" in the past 24 hours, use the following command:

```bash
python3 Stock_scraper.py accounts.txt TSLA 24 hours
```

### Script Output

The script will output the number of times the specified ticker was mentioned in tweets from the specified accounts within the given time interval.

```plaintext
 Hello in the Stock Scrapper

Processing account link: https://twitter.com/example_account
num of tweets found: 10
Found 5 ticker.
...
############################## 

TSLA was mentioned 15 times in the last 24 hours.
```

## Error Handling

If the script encounters any issues (e.g., invalid arguments, missing accounts file, etc.), it will display a usage message:

```plaintext
Usage: python3 Stock_scraper.py accounts.txt Ticker time_interval mins/hours/days/weeks
where:
    time_interval is an integer
    time_unit is one of: mins, hours, days, weeks
    Ticker is a string to search for
    accounts.txt is a path to a file containing list of twitter account links

Example: python3 Stock_scraper.py accounts.txt TSLA 24 hours
```

## Notes

- The script runs Chrome in headless mode to avoid opening a browser window during execution.
- The script handles potential `StaleElementReferenceException` errors that might occur if the DOM updates while processing tweets.
- To avoid bot detection, the script removes certain browser scripts before page loading.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## Authors

- Mostafa Jamal - [GitHub](https://github.com/Mostafa1Jamal1)

---