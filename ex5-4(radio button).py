## Ex 5-4. QRadioButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton , QVBoxLayout


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        rbtn1 = QRadioButton('First Button', self)
        rbtn1.move(50, 50)
        rbtn1.setChecked(True)

        rbtn2 = QRadioButton(self)
        rbtn2.move(50, 70)
        rbtn2.setText('Second Button')

        vbox = QVBoxLayout()
        vbox.addWidget(rbtn1)
        vbox.addWidget(rbtn2)

        rbtn11 = QRadioButton('First Button1', self)
        rbtn11.move(50, 100)

        rbtn22 = QRadioButton(self)
        rbtn22.move(50, 120)
        rbtn22.setText('Second Button1')

        vbox1 = QVBoxLayout()
        vbox1.addWidget(rbtn11)
        vbox1.addWidget(rbtn22)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QRadioButton')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())