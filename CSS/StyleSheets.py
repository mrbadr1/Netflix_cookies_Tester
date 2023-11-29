text_editStylesheet="""
                QTextEdit {
                    background-color: #f2f2f2;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    padding: 5px;
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    color: #333;
                }
            """
ButtonStyleSheet='''
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #4CAF50, stop: 1 #45A049);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #45A049, stop: 1 #4CAF50);
            }
        '''
RadioButtonStyleSheet="""
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    color: #333;
                }
            """
ButtonStyleSheet_GRAY='''
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #4CAF50, stop: 1 #45A049);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #45A049, stop: 1 #4CAF50);
            }
            QPushButton:disabled {
                background-color: gray;
            }
        '''
ComboBoxStyleSheet="""QComboBox{
            background-color: white;
            color: black;
            border: 1px solid #CCCCCC;
            padding: 5px;
            border-radius: 5px;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: #CCCCCC;
            border-left-style: solid;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
        QComboBox::down-arrow {
           image: url(../UI/IMAGES/ARROW.png);
        }
"""
progressbarStyleSheets='''
        QProgressBar {
            background-color: #E0E0E0;
            border: solid white;
            border-radius: 10px;
            color: black;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 10px;
        }
    
    '''

WidgetTableStyleSheet='''
        QTableWidget {
            background-color: white;
            color: black;
            border: 1px solid #CCCCCC;
            border-radius: 5px;
        }
        QTableWidget::item:selected {
            background-color: #E0E0E0;
        }
    '''