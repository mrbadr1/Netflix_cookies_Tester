from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QBrush
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import json
import requests
import sys

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, cookies=cookie_jar)
    return "Netflix" in response.text

class NetflixCookieTester(QWidget):
    def __init__(self):
        super().__init__()

        self.valid = False
        self.account_details = None
        self.file_names = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Netflix Cookie Tester')

        layout = QVBoxLayout()

        self.import_button = QPushButton('Import Cookies', self)
        self.import_button.clicked.connect(self.import_cookies)
        layout.addWidget(self.import_button)

        self.result_layout = QHBoxLayout()
        self.result_label = QLabel('')
        self.result_layout.addWidget(self.result_label)
        self.result_circle = CircleWidget()
        self.result_layout.addWidget(self.result_circle)
        layout.addLayout(self.result_layout)

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

    def import_cookies(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_names, _ = QFileDialog.getOpenFileNames(self, "Import Cookies", "", "Text Files (*.txt);;All Files (*)", options=options)
        if self.file_names:
            self.valid = True
            self.result_label.setText("The Netflix cookies are valid.")
            self.result_circle.set_color(QColor(0, 255, 0))
            self.account_button.setEnabled(True)

            self.update()  # Add this line to trigger a repaint of the widget

    def scrape_account_details(self):
        self.account_details = {}
        for file_name in self.file_names:
            cookies_json = load_cookies_from_file(file_name)
            cookie_jar = json_cookies_to_cookiejar(cookies_json)
            if test_netflix_cookies(cookie_jar):
                url = "https://www.netflix.com/YourAccount"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url, headers=headers, cookies=cookie_jar)
                account_details = {}
                account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
                account_details['Subscription plan'] = scrap(response.text, '<div class="account-section-item" data-uia="plan-label"><b>', '</b>').strip()
                account_details['Next billing date'] = (scrap(response.text, '<div id="" class="account-section-item" data-uia="nextBillingDate-item">','</div>').strip()).split(":")[1].strip()
                account_details['Quality'] =""
                account_details['Member since'] = scrap(response.text, 'class="account-section-membersince--svg"></div>','</div>').strip()

                self.account_details[file_name] = account_details

        self.display_account_details()

    def display_account_details(self):
        self.account_details_table.setRowCount(0)
        for file_name, account_details in self.account_details.items():
            row_position = self.account_details_table.rowCount()
            self.account_details_table.insertRow(row_position)
            self.account_details_table.setItem(row_position, 0, QTableWidgetItem(file_name))
            self.account_details_table.setItem(row_position, 1, QTableWidgetItem(account_details.get('email', '')))

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
        return self.minimumSizeHint()

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        self.setFixedSize(size, size)
        

def main():
    app = QApplication(sys.argv)
    window = NetflixCookieTester()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()