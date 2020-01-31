## Ex 5-12. QPixmap.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyApp(QWidget):

 def __init__(self):
     super().__init__()
     self.initUI()

 def initUI(self):
     pixmap = QPixmap('/home/cho/img_1/horse.13.jpeg')

     lbl_img = QLabel()
     #lbl_img.setPixmap(pixmap)
     #lbl_img.setPixmap(pixmap.scaled(640,480,Qt.KeepAspectRatio,Qt.FastTransformation))
     lbl_img.setPixmap(pixmap.scaledToWidth(1024, Qt.FastTransformation))
     lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
     lbl_size.setAlignment(Qt.AlignCenter)

     vbox = QVBoxLayout()
     vbox.addWidget(lbl_img)
     vbox.addWidget(lbl_size)
     self.setLayout(vbox)

     self.setWindowTitle('QPixmap')
     self.move(300, 300)
     self.show()


if __name__ == '__main__':
 app = QApplication(sys.argv)
 ex = MyApp()
 sys.exit(app.exec_())