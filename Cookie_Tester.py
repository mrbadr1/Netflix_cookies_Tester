import json,requests,sys,os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QSizePolicy,QTextEdit,QDialog,QMessageBox,QApplication, QComboBox ,QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from bs4 import BeautifulSoup
from Functions import *
class CookieTester(QWidget):
    def __init__(self):
        super().__init__()

        self.valid = False
        self.account_details = None
        self.file_names = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Cookie Tester v 1.0')
        self.resize(600, 500)
        layout = QVBoxLayout()

        self.result_layout = QHBoxLayout()
        self.result_label = QLabel('')
        self.result_layout.addWidget(self.result_label)
        self.result_layout.addStretch(1)
        self.result_circle = CircleWidget()
        self.result_layout.addWidget(self.result_circle)
        self.result_layout.addStretch(1)
        layout.addLayout(self.result_layout)

        self.import_button = QPushButton('Import Cookies files', self)
        self.import_button.clicked.connect(self.import_cookies)
        layout.addWidget(self.import_button)
        
        self.import_button = QPushButton('Paste Cookies string', self)
        self.import_button.clicked.connect(self.COOKIE_WINDOW_TOPAST)
        layout.addWidget(self.import_button)

        self.result_label2 = QLabel('')
        self.result_label2.setAlignment(Qt.AlignCenter)
        self.result_label2.setFont(QFont("calibri", 11, QFont.Bold))
        self.result_label2.setVisible(False)
        layout.addWidget(self.result_label2)

        self.cookies_listbox = QComboBox(self)
        self.cookies_listbox.setGeometry(50, 70, 200, 30)
        self.cookies_listbox.setPlaceholderText("Select file...")
        self.cookies_listbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cookies_listbox.setEditable(True)
        self.cookies_listbox.lineEdit().setAlignment(Qt.AlignCenter)
        self.cookies_listbox.lineEdit().setReadOnly(True)
        self.cookies_listbox.lineEdit().setPlaceholderText("Select file...")
        self.cookies_listbox.currentIndexChanged.connect(self.on_cookies_listbox_changed)


        layout.addWidget(self.cookies_listbox)
        
        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("calibri", 16, QFont.Bold))
        layout.addWidget(self.result_label)

        self.account_button2 = QPushButton('convert NETSCAPE to JSON', self)
        self.account_button2.clicked.connect(lambda: self.COOKIE_WINDOW_TOCOPY(self.file_dict[self.cookies_listbox.currentText()]))
        self.account_button2.setVisible(False)
        layout.addWidget(self.account_button2)


        self.account_button = QPushButton('Scrape Account Details', self)
        self.account_button.clicked.connect(self.scrape_account_details)
        self.account_button.setEnabled(False)
        layout.addWidget(self.account_button)

        self.account_details_table = QTableWidget()
        self.account_details_table.setColumnCount(2)
        self.account_details_table.setHorizontalHeaderLabels(['Description', 'Information'])
        self.account_details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.account_details_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.account_details_table)
        self.setLayout(layout)

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
     dialog.setWindowTitle('JSON Cookies')
     dialog.setFixedSize(450,390)
     layout = QVBoxLayout(dialog)

    # Create a QTextEdit widget to display the JSON data
     self.text_edit = QTextEdit(dialog)
     self.text_edit.setReadOnly(False)
     self.text_edit.textChanged.connect(self.set_default_background_color)
     layout.addWidget(self.text_edit)

    # Create a button to test the cookies string
     self.account_button3 = QPushButton('TEST COOKIES', self)
     self.account_button3.clicked.connect(lambda: self.test_cookies_string(self.text_edit.toPlainText()))
     layout.addWidget(self.account_button3)

     self.result_label3 = QLabel('')
     self.result_label3.setAlignment(Qt.AlignCenter)
     self.result_label3.setFont(QFont("calibri", 11, QFont.Bold))
     self.result_label3.setVisible(False)
     layout.addWidget(self.result_label3)
    # Show the dialog
     dialog.exec_()



    def set_default_background_color(self):
                self.text_edit.setStyleSheet("")    
                self.result_label3.setVisible(False)

    def test_cookies_string(self,string):

     try:
      cookies_json = json.loads(string)
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

        # Return the JSON string
        return json_cookies




    def on_cookies_listbox_changed(self, index):
     file_name = self.cookies_listbox.currentText()
     if file_name:
        self.result_circle.set_color(QColor(0, 0, 0))
        self.account_button.setEnabled(False)
        self.account_button2.setVisible(False)
        self.check_cookies(file_name)

    def import_cookies(self):
         options = QFileDialog.Options()
         options |= QFileDialog.ReadOnly
         file_names, _ = QFileDialog.getOpenFileNames(self, "Import Cookies", "", "Text Files (*.txt);;All Files (*)", options=options)
         if file_names:
          self.file_dict = {}
          self.cookies_listbox.clear()
          for file_name in file_names:
            item_name = os.path.basename(file_name)
            self.file_dict[item_name] = file_name
            self.cookies_listbox.addItem(item_name)
            index = self.cookies_listbox.findText(item_name)
            self.result_label.setText(f"")
            self.result_circle.set_color(QColor(0, 0, 0))
            self.account_button2.setVisible(False)
            self.result_label2.setText(f"{len(file_names)} text files imported") # Set the text of result_label2 to show the number of imported text files
            self.result_label2.setVisible(True)

              
    def check_cookies(self, item):
        try:
            index = self.cookies_listbox.findText(item)
            file_name = self.file_dict[item]
            with open(file_name, 'r') as f:
              cookies_json = json.load(f)
            cookie_jar = json_cookies_to_cookiejar(cookies_json)
            valid = test_netflix_cookies(cookie_jar)

            if valid:
                self.result_label.setText(f"cookies are working")
                self.result_circle.set_color(QColor(0, 255, 0))
                self.cookies_listbox.setItemData(index, QBrush(QColor("green")), Qt.BackgroundRole)
                self.valid=True
                self.account_button.setEnabled(True)
            else:
                self.result_label.setText(f"cookies are not working")
                self.cookies_listbox.setItemData(index, QBrush(QColor("red")), Qt.BackgroundRole)
                self.account_button.setEnabled(False)

                self.result_circle.set_color(QColor(255, 0, 0))
        except json.decoder.JSONDecodeError as e:
            if is_netscape_format(file_name):
             self.result_label.setText(f"the file is in netscape format ")
             self.cookies_listbox.setItemData(index, QBrush(QColor("red")), Qt.BackgroundRole)
             self.account_button2.setVisible(True)

            else:
             self.result_label.setText(f"Error loading cookies from file ")
             self.cookies_listbox.setItemData(index, QBrush(QColor("red")), Qt.BackgroundRole)
            self.account_button.setEnabled(False)
            self.result_circle.set_color(QColor(255, 0, 0))
            self.account_button.setEnabled(False)

        except requests.exceptions.RequestException as e:
                error_msg = f"Error connecting ..."
                QMessageBox.critical(self, "Connection Error", error_msg)
                return

    def scrape_account_details(self):
        item= self.cookies_listbox.currentText()
        url = "https://www.netflix.com/YourAccount"
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029. Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5"
         }
        account_details = {}
        try:
                file_name = self.file_dict[item]
                with open(file_name, 'r') as f:
                    cookies_json = json.load(f)
                cookie_jar = json_cookies_to_cookiejar(cookies_json)
                valid = test_netflix_cookies(cookie_jar)

                if valid:
                    response = requests.get(url, headers=headers, cookies=cookie_jar)
                    account_details = {}
                    account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
                    account_details['Subscription plan'] = scrap(response.text, '<div class="account-section-item" data-uia="plan-label"><b>', '</b>').strip()
                    account_details['Member since'] = scrap(response.text, 'class="account-section-membersince--svg"></div>','</div>').strip()
                    
        except requests.exceptions.RequestException as e:
                error_msg = f"Error connecting to {url}: {e}"
                QMessageBox.critical(self, "Connection Error", error_msg)
                return


        except json.decoder.JSONDecodeError as e:
                error_msg = f"Error loading cookies from file {item}: {e}"
                QMessageBox.critical(self, "JSON Error", error_msg)
                return

        self.account_details = account_details
        self.display_account_details()

    def display_account_details(self):
        ##
        self.account_details_table.setRowCount(len(self.account_details))
        row = 0
        for key, value in self.account_details.items():
            self.account_details_table.setItem(row, 0, QTableWidgetItem(key))
            self.account_details_table.setItem(row, 1, QTableWidgetItem(value))
            row += 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(0, 0, 0)

    def set_color(self, color):
        self.color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(0, 0, self.width(), self.height())

    def sizeHint(self):
     return QSize(35, 35)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)

def main():
    app = QApplication(sys.argv)
    window = CookieTester()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
