import json
import requests
import sys
from PyQt5.QtCore import QSize,Qt
from http.cookiejar import CookieJar
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPainter, QColor, QBrush,QFont
from bs4 import BeautifulSoup

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
    response =requests.get(url, headers=headers, cookies=cookie_jar)
    return "Netflix" in response.text


def scrap(html, start, end):
    start_pos = html.find(start)
    if start_pos == -1:
        return ""
    end_pos = html.find(end, start_pos + len(start))
    if end_pos == -1:
        return ""
    return html[start_pos + len(start):end_pos]


class NetflixCookieTester(QWidget):
    def __init__(self):
        super().__init__()

        self.valid = False
        self.account_details = None
        self.file_name = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Netflix Cookie Tester')
        self.resize(600, 400)
        layout = QVBoxLayout()

        self.result_layout = QHBoxLayout()
        self.result_label = QLabel('')
        self.result_layout.addWidget(self.result_label)
        self.result_layout.addStretch(1)
        self.result_circle = CircleWidget()
        self.result_layout.addWidget(self.result_circle)
        self.result_layout.addStretch(1)
        layout.addLayout(self.result_layout)

        self.import_button = QPushButton('Import Cookies file', self)
        self.import_button.clicked.connect(self.import_cookies)
        layout.addWidget(self.import_button)



        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("calibri", 16, QFont.Bold))
        layout.addWidget(self.result_label)


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
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Import Cookies", "", "Text Files (*.txt);;All Files (*)", options=options)
        if self.file_name:
            try:
                with open(self.file_name, 'r') as f:
                    cookies_json = json.load(f)
                cookie_jar = json_cookies_to_cookiejar(cookies_json)
                self.valid = test_netflix_cookies(cookie_jar)

                if self.valid:
                    self.result_label.setText("The Netflix cookies are valid.")
                    self.valid = True
                    self.result_circle.set_color(QColor(0, 255, 0))
                    self.account_button.setEnabled(True)
                else:
                    self.result_label.setText("The Netflix cookies are not valid.")
                    self.result_circle.set_color(QColor(255, 0, 0))
                    self.account_button.setEnabled(False)

                self.update()  # Add this line to trigger a repaint of the widget
            except json.decoder.JSONDecodeError as e:
                print(f"Error loading cookies from file {self.file_name}: {e}")
                self.result_label.setText("Error loading cookies from file.")
                self.result_circle.set_color(QColor(255, 0, 0))
                self.account_button.setEnabled(False)
                self.update()  # Add this line to trigger a repaint of the widget

    def scrape_account_details(self):
        url = "https://www.netflix.com/YourAccount"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        cookie_jar = json_cookies_to_cookiejar(load_cookies_from_file(self.file_name))
        response = requests.get(url, headers=headers, cookies=cookie_jar)

        account_details = {}
        account_details['Email'] = scrap(response.text, '<div data-uia="account-email" class="account-section-item account-section-email">', '</div>').strip()
        account_details['Subscription plan'] = scrap(response.text, '<div class="account-section-item" data-uia="plan-label"><b>', '</b>').strip()
        account_details['Member since'] = scrap(response.text, 'class="account-section-membersince--svg"></div>','</div>').strip()

        self.account_details = account_details
        self.display_account_details()

    def display_account_details(self):
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
     return QSize(25, 25)

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
