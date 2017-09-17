import sys
import qdarkstyle
import os
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QRadioButton, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt

from filter_content import FilterContent
from match_users import MatchUsers
from collect_content import ContentCollector


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'TrollHuntr'
        self.left = 380
        self.top = 150
        self.width = 550
        self.height = 450
        self.setFixedSize(self.size())
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        newFont = QFont("Courier", 65, QFont.Bold)
        self.label = QLabel("TrollHuntr",self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(0,20)
        self.label.resize(650,100)
        self.label.setFont(newFont)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 130)
        self.textbox.resize(600, 35)
        self.textbox.setAlignment(Qt.AlignCenter)

        # Create a button in the window
        self.button = QPushButton('Compare', self)
        self.button.move(260, 440)

        self.radiobutton1 = QRadioButton("Search", self)
        self.radiobutton1.setChecked(True)
        self.radiobutton1.saved = True
        self.radiobutton1.move(260,380)

        self.radiobutton2 = QRadioButton("New Search", self)
        self.radiobutton2.saved = False
        self.radiobutton2.toggled.connect(self.on_radio_button_toggled)
        self.radiobutton2.move(260, 405)

        self.troll = QLabel(self)
        pixmap = QPixmap('troll.png')
        pixmap = pixmap.scaled(200,200)
        self.troll.setPixmap(pixmap)
        self.troll.move(210,170)
        self.troll.resize(200,200)

        # connect button to function on_click
        self.button.clicked.connect(self.get_matches)
        self.show()

    def on_radio_button_toggled(self):
        radiobutton = self.sender()

        if radiobutton.isChecked():
            QMessageBox.warning(self, "",
                                "Are you sure you want to do a new search?\nGathering data again will take some time.",
                                QMessageBox.Ok, QMessageBox.NoButton)
    @pyqtSlot()
    def get_matches(self):
        if(self.textbox.text() == ""):
            QMessageBox.warning(self, "",
                                "Please enter a valid subreddit",
                                QMessageBox.Ok, QMessageBox.NoButton)
            return
        if self.radiobutton2.isChecked() and self.file_exists:
            os.remove(self.textbox.text().lower()+"_data.txt")
            os.remove(self.textbox.text().lower()+"_filter.txt")
        ContentCollector(self.textbox.text().lower())
        FilterContent(self.textbox.text().lower()).get_data()
        self.secondScreen = Widget(info = MatchUsers(self.textbox.text().lower()).match_results())
        self.secondScreen.show()

    def file_exists(self):
        if os.path.exists(self.SUBREDDIT + '_filter.txt'):
            logger.warning("Opened")
            return True


class Widget(QWidget):
    def __init__(self, info=None, parent=None):
        super(Widget, self).__init__()
        # Container Widget
        widget = QWidget()
        widget.setGeometry(0, 0,600, 435)
        # Layout of Container Widget
        layout = QVBoxLayout(self)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(len(info))
        tableWidget.setColumnCount(3)
        tableWidget.setItem(0, 0, QTableWidgetItem("Troll"))
        tableWidget.setItem(0, 1, QTableWidgetItem("Main Account"))
        tableWidget.setItem(0, 2, QTableWidgetItem("Sample Comment"))
        y = 1
        for item in info:
            tableWidget.setItem(y, 0, QTableWidgetItem(item['throw']))
            tableWidget.setItem(y, 1, QTableWidgetItem(item['match']))
            tableWidget.setItem(y, 2, QTableWidgetItem(item['comment']))
            y += 1
        tableWidget.resize(600,500)
        tableWidget.itemDoubleClicked.connect(self.open_link)
        header = tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
        layout.addWidget(tableWidget)

        widget.setLayout(layout)

        # Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        # Scroll Area Layer add
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
        self.setGeometry(380,150,640,480)

    def open_link(self, item):
        webbrowser.open('http://www.reddit.com/user/' + item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())
