Netflix Cookie Tester

WARNING: Use at your own risk. This tool is for educational purposes only.
The Netflix Cookie Tester is a Python-based tool that allows you to test Netflix cookies to see if they are still valid and working. It also provides the ability to scrape account details from the Netflix account associated with the cookie.

Requirements

- Python 3.x
- PyQt5
- requests

Installation
------------------------
Clone the repository to your local machine.

Install the required packages by running the following command in your terminal: 
,,,
pip install -r requirements.txt
,,,

Usage

Launch the tool by running the following command in your terminal: 
,,,
python netflix_cookie_tester.py
,,,
Click the "Import Cookies" button to select the text file containing the Netflix cookie(s) you want to test.
Click the "Scrape Account Details" button to test the cookies and scrape the associated Netflix account details.
The tool will display the number of non-working cookies and the associated account details (if available) in a table.
How it works
The Netflix Cookie Tester works by testing the validity of the Netflix cookie(s) provided by the user. It does this by sending a GET request to the Netflix homepage with the cookie(s) attached to the request. If the response contains the text "Who's watching?", the cookie(s) are considered valid.
If the cookie(s) are valid, the tool then sends a GET request to the Netflix account page with the cookie(s) attached to the request. It then scrapes the HTML response for the associated account details, such as the email address, subscription plan, next billing date, quality, and member since date.
Limitations
The Netflix Cookie Tester has a few limitations:
It only works with Netflix cookies.
It only tests the validity of the cookie(s) and does not guarantee access to the associated Netflix account.
It may not work with all versions of Netflix or all Netflix regions.
It may not work with all types of Netflix accounts (e.g. trial accounts).

Contributing

Contributions to the Netflix Cookie Tester are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

License

The Netflix Cookie Tester is licensed under the MIT License. See the LICENSE file for more information.