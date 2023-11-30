Cookie Tester
--------

![Example screenshot](ScreenShots3.png)



WARNING: Use at your own risk. This tool is for educational purposes only.

The Cookie Tester is a Python-based tool that allows you to test  cookies to see if they are still valid and working. It also provides the ability to scrape account details from the account associated with the cookie.

Installation
------------------------
Clone the repository to your local machine.

Usage
------------------------

Launch the tool by running the following command in your terminal: 
,,,
python main.py
,,,
Click the "Import Cookies" button to select the folder with text files(Txt Format) containing the  cookie(s) you want to test.

The tool will display the number of non-working cookies and the associated account details (if available) in a table.
How it works
The  Cookie Tester works by testing the validity of the cookie(s) provided by the user. It does this by sending a GET request to the  homepage with the cookie(s) attached to the request. 

If the cookie(s) are valid, the tool then sends a GET request to the account page with the cookie(s) attached to the request. It then scrapes the HTML response for the associated account details, such as the email address, subscription plan, quality, profiles number, and member since date.

Contributing

Contributions to the Cookie Tester are welcome! If you find a bug or have an idea for a new feature, please open an issue or submit a pull request.

License

The Cookie Tester is licensed under the MIT License. See the LICENSE file for more information.
