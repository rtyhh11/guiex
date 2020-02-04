import sys
import cv2
import numpy as np
from PyQt5.QtGui import QIcon, QImage, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QAction, QFileDialog, qApp
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.openFile)


        exitAction = QAction(QIcon('/home/park/Downloads/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openFile)
        filemenu.addAction(exitAction)

        self.width = 640
        self.height = 640
        self.channel = 3
        self.cvImage = np.ones((self.width, self.height, self.channel), np.uint8) * 255
        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)


        self.mQImage = QImage(self.cvImage, self.width, self.height, self.cvImage.strides[0], QImage.Format_RGB888)
        self.mQImage.scaledToWidth(640, Qt.FastTransformation)


        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        winHeight = 600
        winWidth = 800
        self.resize(winWidth, winHeight)
        self.show()

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        print('debug:'+fname[0])
        if fname[0]:
            self.cvImage = cv2.imread(fname[0])
            resizeImage = cv2.resize(self.cvImage, dsize=(self.width, self.height))
            RGBImage = cv2.cvtColor(resizeImage, cv2.COLOR_BGR2RGB)
            self.mQImage = QImage(RGBImage, self.width, self.height, RGBImage.strides[0], QImage.Format_RGB888)
            #plt.imshow(RGBImage)
            #plt.show()
            self.update()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())