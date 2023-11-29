import json,requests,sys,os,threading,time,re,calendar
from http.cookiejar import CookieJar
from PyQt5.QtCore import QThread, QUrl, Qt, pyqtSignal,QTimer
from PyQt5.QtWidgets import (QProgressBar, QAbstractItemView, QSizePolicy, QTextEdit, QDialog, QMessageBox,
                             QRadioButton, QApplication, QComboBox, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor, QLinearGradient, QDesktopServices
from bs4 import BeautifulSoup
from alive_progress import alive_bar
from PyQt5.QtCore import QThread, pyqtSignal,QTimer
from logic.gui_functions import *
from CSS.StyleSheets import *
# Global variables

account_details = {}
folder_path = ""
working_cookies = 0
Dead_cookies = 0
total_files = 0