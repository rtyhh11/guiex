import sys
from _curses import is_term_resized
import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox ,QFileDialog , QTextEdit , QPushButton ,QComboBox, QLineEdit
from PyQt5.QtCore import Qt ,QItemSelection, QModelIndex
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem , QIntValidator
from PIL import Image

class MyApp(QWidget):

    is_resize = False
    is_rotate = False
    is_hfilp = False
    is_vfilp = False

    img_fomat = '(*.jpg , *.png , *.jpeg)'
    img_fomat_extension = ('.jpg' , '.png' , '.jpeg')
    file_paths = ()
    rotate_data = 90

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Resize
        cb = QCheckBox('Resize', self)
        cb.move(20, 20)
        cb.stateChanged.connect(self.ischeckResize)

        self.le_width = QLineEdit(self)
        self.le_width.setGeometry(120 ,20 , 80 ,20)
        self.le_width.setValidator(QIntValidator(0,9999))

        self.le_height = QLineEdit(self)
        self.le_height.setGeometry(210, 20, 80, 20)
        self.le_height.setValidator(QIntValidator(0, 9999))

        #Rotate
        cb1 = QCheckBox('Rotate', self)
        cb1.move(20, 60)
        cb1.stateChanged.connect(self.ischeckRotate)

        combo = QComboBox(self)
        combo.addItem('90')
        combo.addItem('180')
        combo.addItem('270')
        combo.move(120, 60)
        combo.activated[str].connect(self.onActivated)


        #hflip
        cb2 = QCheckBox('hflip', self)
        cb2.move(20, 100)
        cb2.stateChanged.connect(self.ischeckHfilp)

        #vflip
        cb3 = QCheckBox('vflip', self)
        cb3.move(20, 140)
        cb3.stateChanged.connect(self.ischeckVfilp)

        #set path
        btn_path = QPushButton(self)
        btn_path.move(20,180)
        btn_path.setText('set file path')
        btn_path.clicked.connect(self.setFilePath)

        btn_path_delete = QPushButton(self)
        btn_path_delete.move(180, 180)
        btn_path_delete.setText('Delete file path')
        btn_path_delete.clicked.connect(self.deleteFilePath)

        self.listview = QListView(self)
        self.model = QStandardItemModel()
        self.listview.setGeometry(20, 220, 360, 100)


        '''
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(20,220,260,100)
        '''

        #run
        btn_run = QPushButton(self)
        btn_run.setGeometry(300, 20, 80 , 80)
        btn_run.setText('Run')
        btn_run.clicked.connect(self.file_change)

        self.setWindowTitle('quiz3')
        self.setGeometry(300, 300, 400, 500)
        self.show()

    def ischeckResize(self, state):
        if state == Qt.Checked:
            self.is_resize = True
        else:
            self.is_resize = False

    def ischeckRotate(self, state):
        if state == Qt.Checked:
            self.is_rotate = True
        else:
            self.is_rotate = False

    def ischeckHfilp(self, state):
        if state == Qt.Checked:
            self.is_hfilp = True
        else:
            self.is_hfilp = False

    def ischeckVfilp(self, state):
        if state == Qt.Checked:
            self.is_vfilp = True
        else:
            self.is_vfilp = False

    def onActivated(self,text):
        self.rotate_data = int(text)


    def setFilePath(self):
        #self.textEdit.setText('')
        fname = QFileDialog.getOpenFileNames(self, 'Open file', './',self.img_fomat)
        for a in fname[0] :
            #self.textEdit.setText(self.textEdit.toPlainText()+'\n'+a)
            self.model.appendRow(QStandardItem(a))
        self.listview.setModel(self.model)

        #self.file_paths = fname[0]

        # for path in self.file_paths:
        #     print(path)

    def deleteFilePath(self):
        delete_item = self.listview.currentIndex().row()
        self.model.removeRow(delete_item)

    def file_change(self):
        if self.is_rotate :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgRotate(path)
            # for path in self.file_paths:
            #     self.setImgRotate(path)
        if self.is_resize :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgResize(path)
            # for path in self.file_paths:
            #     self.setImgResize(path)
        if self.is_vfilp :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgFlip(path,'v')
            # for path in self.file_paths:
            #     self.setImgFlip(path,'v')
        if self.is_hfilp :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgFlip(path,'h')
            # for path in self.file_paths:
            #     self.setImgFlip(path,'h')


    def setImgResize(self , path):
        ## file name
        #print(path)
        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        resize_file_name = file_name[0:extension_idx] \
                           + '_resize_' \
                           +file_name[extension_idx : len(file_name)]

        ## file resize
        img = Image.open(path)
        w = img.width
        h = img.height

        resize_width = int(self.le_width.text())
        resize_height = int(self.le_height.text())

        cvImage = np.ones((w,h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        resizeImage = cv2.resize(img_cv, dsize=(resize_width,resize_height))
        cv2.imwrite(path[0:name_idx] + resize_file_name,resizeImage)


    def setImgRotate(self , path):
        ## file name
        #print(path)
        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        rotate_file_name = file_name[0:extension_idx] \
                           + '_rotate_{}'.format(self.rotate_data) \
                           +file_name[extension_idx : len(file_name)]

        ## file rotate
        img = Image.open(path)
        w = img.width
        h = img.height

        cvImage = np.ones((w,h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        resizeImage = cv2.resize(img_cv, dsize=(2*w, 2*h))
        M = cv2.getRotationMatrix2D((w , h), self.rotate_data, 0.5)
        #M = cv2.getRotationMatrix2D((w, h), self.rotate_data, 1)
        rotated = cv2.warpAffine(img_cv, M, (w, h))
        cv2.imwrite(path[0:name_idx] + rotate_file_name,rotated)


    def setImgFlip(self , path,mode):
        ## file name
        #print(path)
        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        resize_file_name = file_name[0:extension_idx] \
                           + '_{}flip_'.format(mode) \
                           +file_name[extension_idx : len(file_name)]

        ## file flip
        img = Image.open(path)
        w = img.width
        h = img.height

        cvImage = np.ones((w,h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        if 'v' in mode :
            flipImage = cv2.flip(img_cv,1)
        elif 'h' in mode :
            flipImage = cv2.flip(img_cv, 0)

        cv2.imwrite(path[0:name_idx] + resize_file_name,flipImage)


    def seach_filename(self , path):
        str = path
        result = 0
        while True:
            idx = str.find('/')
            if idx > -1:
                #print(idx)
                str = str[idx+1 : len(str)]
                result += idx + 1
            else :
                break
        return result

    def seach_extension(self, name):
        for extension in self.img_fomat_extension :
            extension_idx = name.find(extension)
            if extension_idx > -1 :
                return extension_idx



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())