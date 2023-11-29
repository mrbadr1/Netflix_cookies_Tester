from config import *

def clear_text_edit(self):
   self.text_edit.clear()
def test_all_cookies(self):
    global total_files
    global Dead_cookies
    global working_cookies
    global total_files
    Dead_cookies = 0
    working_cookies = 0
    self.test_button.setEnabled(False)
    self.test_button.setText("CHECKING...")
    total_files = self.cookies_listbox.count()
    self.progress_bar_main.setRange(0, total_files)
    self.progress_bar_main.setValue(0)
    self.progress_bar_main.show()

    # Create and start the background task
    for index in range(total_files):
        self.current_label.setText(f'CHECKING|"{index+1}/{total_files}"|"{self.cookies_listbox.itemText(index)}"')
        self.current_label.setVisible(True)
        QApplication.processEvents()
        self.check_cookies(index)
        self.progress_bar_main.setValue(index + 1)
        self.test_button.setText("CHECKING ...")
        QApplication.processEvents()

    self.current_label.setText(f'Checking completed')
    self.current_label.setVisible(False)
    self.progress_bar_main.hide()
    self.result_label.setText(f'🟢Working: {working_cookies}  🔴Dead: {Dead_cookies}')
    self.test_button.setEnabled(True)
    self.test_button.setText("CHECK ALL COOKIES")
def test_cookies(self):
    cookies_string = self.text_edit.toPlainText()
    if cookies_string is None or cookies_string.strip() == "":
        error_msg = f"Cookies string is empty."
        QMessageBox.critical(self, "Text Error", error_msg)
        return
    if self.json_radio.isChecked():
        #test make sure its json format
        self.test_cookies_json(cookies_string)
    else:
        #test make sure its netscape
        self.test_netflix_cookies_netscape(cookies_string)
def test_cookies_json(self, cookies_string):
    try:
     cookies_jsond = json.loads(cookies_string)
     cookie_jarr = json_cookies_to_cookiejar(cookies_jsond)
     if test_netflix_cookies(cookie_jarr):
           # Set the background color of the text_edit widget to green
           self.text_edit.setStyleSheet("background-color: green;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("cookies working")
     else:
           # Reset the background color of the text_edit widget
           self.text_edit.setStyleSheet("background-color: red;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("cookies not working")
    except json.JSONDecodeError:
        
     error_msg = "Invalid JSON format."
     QMessageBox.critical(self, "Format Error", error_msg)
    except json.decoder.JSONDecodeError as e:
           self.text_edit.setStyleSheet("background-color: red;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("format error")      
    except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting ..."
            QMessageBox.critical(self, "Connection Error", error_msg)
            return
def is_netscape(self, cookies_string):
        if not cookies_string.startswith(".") and "\t" not in cookies_string:                
            error_msg = "Invalid Netscape format"
            QMessageBox.critical(self, "Format Error", error_msg)
          
def open_text_file(self):
    selected_rows = self.account_details_table.selectionModel().selectedRows()
    if selected_rows:
        selected_row = selected_rows[0].row()
        file_column_index = -1
        for column in range(self.account_details_table.columnCount()):
            header_name = self.account_details_table.horizontalHeaderItem(column).text()
            if header_name == "file":
                file_column_index = column
                break
        if file_column_index != -1:
            file_path = self.account_details_table.item(selected_row, file_column_index).text()
            if os.path.exists(file_path):
                try:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
                except Exception as e:
                    print("Error opening file:", str(e))
            else:
                print("File path does not exist.")
        else:
            print("File column not found.")
    else:
        print("No row selected.")
         
def test_netflix_cookies_netscape(self, cookies_string):
    self.is_netscape(cookies_string)
 # Split the data into individual cookies
    lines = cookies_string.strip().split('\n')
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
    try:
         cookies_jsond = json.loads(cookies_json)
         cookie_jarr = json_cookies_to_cookiejar(cookies_jsond)
          
         if cookies_string.startswith(".") and "\t" in cookies_string and test_netflix_cookies(cookie_jarr):
           # Set the background color of the text_edit widget to green
           self.text_edit.setStyleSheet("background-color: green;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("cookies working")
         else:
           # Reset the background color of the text_edit widget
           self.text_edit.setStyleSheet("background-color: red;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("cookies not working")
    except json.decoder.JSONDecodeError as e:
           self.text_edit.setStyleSheet("background-color: red;")
           self.result_label3.setVisible(True)
           self.result_label3.setText("format error")      
    except requests.exceptions.RequestException as e:
                   error_msg = f"Error connecting ..."
                   QMessageBox.critical(self, "Connection Error", error_msg)
                   return
   
def set_default_background_color(self):
            self.text_edit.setStyleSheet("")    
            self.result_label3.setVisible(False)
def test_cookies_string(self,string):
 json_cookies =self.convert_netscape_to_json_text(string)
 try:
  cookies_json = json.loads(json_cookies)
  cookie_jar = json_cookies_to_cookiejar(cookies_json)
  if not string.startswith(".") and "\t" not in string and test_netflix_cookies(cookie_jar):
    # Set the background color of the text_edit widget to green
    self.text_edit.setStyleSheet("background-color: green;")
    self.result_label3.setVisible(True)
    self.result_label3.setText("cookies working")
  else:
    # Reset the background color of the text_edit widget
    self.text_edit.setStyleSheet("background-color: red;")
    self.result_label3.setVisible(True)
    self.result_label3.setText("cookies not working")
 except json.decoder.JSONDecodeError as e:
    self.text_edit.setStyleSheet("background-color: red;")
    self.result_label3.setVisible(True)
    self.result_label3.setText("format error")      
 except requests.exceptions.RequestException as e:
            error_msg = f"Error connecting ..."
            QMessageBox.critical(self, "Connection Error", error_msg)
            return
def convert_netscape_to_json(self,file_path):
 with open(file_path, "r+") as file:
    netscape_data = file.read()
 # Split the data into individual cookies
    lines = netscape_data.strip().split('\n')
 # Create an empty list to store the JSON data
    cookies = []
 # Loop through each cookie and add it to the JSON list
    for line in lines:
      if line.startswith('.netflix.com'):
         parts = line.strip().split('\t')
         cookie = {
        'domain': parts[0],
        'path': parts[2],
        'name': parts[5],
        'value': parts[6]
         }
         cookies.append(cookie)
    json_cookies = json.dumps(cookies)
    # Ask the user if they want to save the new JSON file in the original text file
    reply = QMessageBox.question(self,'Save JSON file', 'Do you want to save the new JSON file in the original text file?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        # Write the JSON string back to the file
        file.seek(0)
        file.write(json_cookies)
        file.truncate()
    print(json_cookies)
    # Return the JSON string
    return json_cookies
def convert_netscape_to_json_text(self,text):
 # Split the data into individual cookies
    lines = text.strip().split('\n')
 # Create an empty list to store the JSON data
    cookies = []
 # Loop through each cookie and add it to the JSON list
    for line in lines:
      if line.startswith('.netflix.com') or line.startswith('.www.netflix.com'):
         parts = line.strip().split('\t')
         cookie = {
        'domain': parts[0],
        'path': parts[2],
        'name': parts[5],
        'value': parts[6]
         }
         cookies.append(cookie)
    json_cookies = json.dumps(cookies)
    # Return the JSON string
    return json_cookies
def on_cookies_listbox_changed(self, index):
 file_name = self.cookies_listbox.currentText()
 if file_name:
    self.check_cookies(file_name)
def import_cookies(self):
    global folder_path
    global Dead_cookies
    global working_cookies
    Dead_cookies=0
    working_cookies=0
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    folder_path = QFileDialog.getExistingDirectory(self, "Import Cookies", options=options)
    if folder_path:
        self.file_dict = {}
        self.cookies_listbox.clear()
        file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt')]
        for file_name in file_names:
            item_name = os.path.basename(file_name)
            self.file_dict[item_name] = os.path.join(folder_path, file_name)
            self.cookies_listbox.addItem(item_name)
        self.result_label.setText("")
        self.result_label2.setText(f"{len(file_names)} Text files")  # Set the text of result_label2 to show the number of imported text files
        self.result_label2.setVisible(True)
    QApplication.processEvents()
          
def check_cookies(self, INDEX):
    global working_cookies
    global Dead_cookies
    try:
        item = self.cookies_listbox.itemText(INDEX)
        file_path = self.file_dict.get(item)
        file_path = os.path.normpath(file_path)
        with open(file_path, "r") as file:
            text = file.read()
            lines = text.strip().split('\n')
            cookies = []
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
            cookies_jsond = json.loads(cookies_json)
            cookie_jarr = json_cookies_to_cookiejar(cookies_jsond)

            if test_netflix_cookies(cookie_jarr):
                working_cookies += 1
                account_details = self.scrape_account_details(cookies_jsond, file_path)
                thread = threading.Thread(target=self.display_account_details(account_details))
                thread.start()
                self.cookies_listbox.setItemData(INDEX, QBrush(QColor("green")), Qt.BackgroundRole)
                self.valid = True
            else:
                Dead_cookies += 1
                self.cookies_listbox.setItemData(INDEX, QBrush(QColor("red")), Qt.BackgroundRole)
            QApplication.processEvents()
    except json.decoder.JSONDecodeError as e:
        if is_netscape_format(file_path):
            self.result_label.setText(f"The file is in netscape format ... ")
            self.cookies_listbox.setItemData(INDEX, QBrush(QColor("red")), Qt.BackgroundRole)
        else:
            self.result_label.setText(f"Error loading cookies from file ")
            self.cookies_listbox.setItemData(INDEX, QBrush(QColor("red")), Qt.BackgroundRole)
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting ..."
        QMessageBox.critical(self, "Connection Error", error_msg)
        return

def scrape_account_details(self,cookies_json, path):

            url = "https://www.netflix.com/YourAccount"
            headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029. Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5"
    }
            global account_details
            account_details = {}
            cookie = json_cookies_to_cookiejar(cookies_json)
            response = requests.get(url, headers=headers, cookies=cookie)
            account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
            account_details['Subscription plan'] = scrap(response.text, '<div class="account-section-item" data-uia="plan-label"><b>', '</b>').strip()
            account_details['Membership'] = scrap(response.text, 'class="account-section-membersince--svg"></div>','</div>').strip()
            account_details['Profils'] = len(BeautifulSoup(response.content, "html.parser").find_all("li", class_="single-profile"))
            account_details['file']=path
            member_since = account_details['Membership']
            matches = re.findall(r'[A-Za-z]+\s+\d{4}', member_since)
            if matches:
                month_year = matches[0]
                # Rest of your code for converting the month and formatting the 'Membership' value
            else:
                # Handle the case when no matches are found
                month_year = "Unknown"
            # Converting the month to English
            month_dict = {v.lower(): k for k, v in enumerate(calendar.month_name)}
            for month, month_num in month_dict.items():
                month_year = month_year.replace(month, calendar.month_name[month_num])
            
            # Formatting the 'Membership' value as desired
            formatted_member = '-'.join(month_year.split()[::-1])
            
            # Updating the 'Membership' value in the dictionary
            account_details['Membership'] = formatted_member
            return account_details
def display_account_details(self, account_details):
    row_count = self.account_details_table.rowCount()
    self.account_details_table.setRowCount(row_count + 1)
    for column, (header, value) in enumerate(account_details.items()):
        if header == 'Profils':
            value = str(value)
        item = QTableWidgetItem(value)
        item.setTextAlignment(Qt.AlignCenter)  # Align the text to the center
        self.account_details_table.setItem(row_count, column, item)
        self.account_details_table.item(row_count, column).setBackground(QColor(240, 240, 240))  # Set background color
        self.account_details_table.item(row_count, column).setForeground(QColor(0, 0, 0))  # Set text color
        self.account_details_table.item(row_count, column).setFont(QFont("Calibri", 11))  # Set font style

    if header == 'Email':
        self.account_details_table.item(row_count, column).setTextAlignment(Qt.AlignLeft)  # Align email text to the left
        self.account_details_table.item(row_count, column).setFont(QFont("Calibri", 8))  # Set font style
    if header == 'file':
       self.account_details_table.item(row_count, column).setFont(QFont("Calibri", 8))  # Set font style
    # Resize the email column to fit the content
    self.account_details_table.resizeColumnsToContents()
def refresh_app(self):
    # This function will be called every 10 milliseconds
    QApplication.processEvents()
def start_running_task(self):
    thread = QThread()
    thread.started.connect(self.start_running_task)
    thread.start()
def COOKIE_WINDOW_TOCOPY(self,PATH):
    # Create a QDialog to display the JSON data
    dialog = QDialog(self)
    dialog.setWindowTitle('JSON Cookies')
    layout = QVBoxLayout(dialog)
    # Create a QTextEdit widget to display the JSON data
    text_edit = QTextEdit(dialog)
    text_edit.setReadOnly(True)
    layout.addWidget(text_edit)
    # Call the function to convert the Netscape file to JSON
    json_cookies = self.convert_netscape_to_json(PATH)
    # Insert the JSON data into the QTextEdit widget
    text_edit.insertPlainText(json_cookies)
    # Show the dialog
    dialog.exec_()
def COOKIE_WINDOW_TOPAST(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('COOKIES STRING')
        dialog.setFixedSize(490, 490)
        layout = QVBoxLayout(dialog)
        # Create a QTextEdit widget to display the JSON data
        self.text_edit = QTextEdit(dialog)
        self.text_edit.setReadOnly(False)
        self.text_edit.textChanged.connect(self.set_default_background_color)
        # Apply modern styling using CSS
        self.text_edit.setStyleSheet(text_editStylesheet)
        # Set the text edit's vertical scrollbar policy
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # Add the text edit widget to the layout
        layout.addWidget(self.text_edit)
        # Create a QHBoxLayout to hold the radio buttons
        radio_layout = QHBoxLayout()
        # Create radio buttons for choosing between Netscape and JSON format
        # Create the QRadioButtons for Netscape and JSON formats
        self.netscape_radio = QRadioButton('Netscape Format', dialog)
        self.json_radio = QRadioButton('JSON Format', dialog)
        self.netscape_radio.setChecked(True)  # Set Netscape as the default option
        # Apply modern styling using CSS
        self.netscape_radio.setStyleSheet(RadioButtonStyleSheet)
        self.json_radio.setStyleSheet(RadioButtonStyleSheet)
        # Add the radio buttons to the radio layout
        radio_layout.addWidget(self.netscape_radio)
        radio_layout.addWidget(self.json_radio)
        # Set the alignment of the radio layout
        radio_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(radio_layout)
        # Create a button to test the cookies string
        self.account_button3 = QPushButton('TEST COOKIES', dialog)
        self.account_button3.clicked.connect(self.test_cookies)
        self.account_button3.setStyleSheet(ButtonStyleSheet)
        layout.addWidget(self.account_button3)
        # Create a button to clear the text_edit widget
        self.clear_button = QPushButton('CLEAR TEXT', dialog)
        self.clear_button.clicked.connect(self.clear_text_edit)
        self.clear_button.setStyleSheet(ButtonStyleSheet)
        layout.addWidget(self.clear_button)
        self.clear_button = QPushButton('SAVE TEXT', dialog)
        self.clear_button.setStyleSheet(ButtonStyleSheet)
        layout.addWidget(self.clear_button)
        self.result_label3 = QLabel('')
        self.result_label3.setAlignment(Qt.AlignCenter)
        self.result_label3.setFont(QFont("calibri", 11, QFont.Bold))
        self.result_label3.setVisible(False)
        layout.addWidget(self.result_label3)
        # Show the dialog
        dialog.exec_()
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
    return "whos.watching" in response.text

def scrap(html, start, end):
    start_pos = html.find(start)
    if start_pos == -1:
        return ""
    end_pos = html.find(end, start_pos + len(start))
    if end_pos == -1:
        return ""
    return html[start_pos + len(start):end_pos]