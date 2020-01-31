## Ex 5-5. QComboBox.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    status = 'mm'

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # input
        self.cb = QComboBox(self)
        self.cb.addItem('mm')
        self.cb.addItem('cm')
        self.cb.activated[str].connect(self.onActivated)


        self.le1 = QLineEdit(self)
        self.le1.textChanged.connect(self.changeLabelText)

        grid.addWidget(self.le1, 0, 0)
        grid.addWidget(self.cb, 0, 1)

        # output
        self.lb11 = QLabel('', self)
        self.lb11.setAlignment(Qt.AlignCenter)

        self.lb12 = QLabel('mm', self)
        self.lb12.setAlignment(Qt.AlignCenter)

        self.lb21 = QLabel('', self)
        self.lb21.setAlignment(Qt.AlignCenter)

        self.lb22 = QLabel('cm', self)
        self.lb22.setAlignment(Qt.AlignCenter)

        grid.addWidget(self.lb11, 1, 0)
        grid.addWidget(self.lb12, 1, 1)
        grid.addWidget(self.lb21, 2, 0)
        grid.addWidget(self.lb22, 2, 1)

        self.setWindowTitle('cal')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onActivated(self, text):
        self.status = text
        self.changeLabel()

    def changeLabel(self ):
        try:
            num = float(self.le1.text())

            if self.status in 'cm':
                self.lb11.setText(str(num * 10))
                self.lb11.adjustSize()

                self.lb21.setText(str(num))
                self.lb21.adjustSize()

            if self.status in 'mm':
                self.lb11.setText(str(num))
                self.lb11.adjustSize()

                self.lb21.setText(str(num / 10))
                self.lb21.adjustSize()

        except ValueError :
            self.lb11.setText('')
            self.lb11.adjustSize()

            self.lb21.setText('')
            self.lb21.adjustSize()

    def changeLabelText(self):
        self.changeLabel()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
