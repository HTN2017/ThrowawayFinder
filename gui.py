import sys
import qdarkstyle
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QRadioButton, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt


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

        newFont = QFont("Courier", 90, QFont.Bold)
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

        radiobutton = QRadioButton("Search", self)
        radiobutton.setChecked(True)
        radiobutton.saved = True
        radiobutton.move(260,380)

        radiobutton = QRadioButton("New Search", self)
        radiobutton.saved = False
        radiobutton.toggled.connect(self.on_radio_button_toggled)
        radiobutton.move(260, 405)

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
        self.secondScreen = Widget()
        self.secondScreen.show()


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__()
        # Container Widget
        widget = QWidget()
        # Layout of Container Widget
        layout = QVBoxLayout(self)

        tableWidget = QTableWidget()
        tableWidget.setRowCount(1)
        tableWidget.setColumnCount(3)
        tableWidget.setItem(0, 0, QTableWidgetItem("Troll"))
        tableWidget.setItem(0, 1, QTableWidgetItem("Comment"))
        tableWidget.setItem(0, 2, QTableWidgetItem("Main Account"))
        tableWidget.resize(600,500)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = App()
    sys.exit(app.exec_())
