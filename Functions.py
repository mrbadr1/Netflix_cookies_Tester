import json
import requests
from http.cookiejar import CookieJar

def is_netscape_format(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    # Check if the data starts with a domain name
    if data.startswith("."):
        # Check if the data contains at least one tab character
        if "\t" in data:
            return True
    return False

def load_cookies_from_file(file_path):
    with open(file_path, 'r') as f:
        cookies_json = json.load(f)
    return cookies_json


def json_cookies_to_cookiejar(json_cookies):
    cookie_jar = CookieJar()
    for cookie in json_cookies:
        cookie_jar.set_cookie(requests.cookies.create_cookie(**cookie))
    return cookie_jar


def test_netflix_cookies(cookie_jar):
    url = "https://www.netflix.com/browse"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029. Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5"
         }
    response = requests.get(url, headers=headers, cookies=cookie_jar)
    return "YourAccount" in response.text

def scrap(html, start, end):
    start_pos = html.find(start)
    if start_pos == -1:
        return ""
    end_pos = html.find(end, start_pos + len(start))
    if end_pos == -1:
        return ""
    return html[start_pos + len(start):end_pos]
