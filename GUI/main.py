#!/usr/bin/python
# encoding: utf-8
import sys
from subprocess import Popen
from PyQt4 import QtGui
import main_ui


class MyMainWindow(QtGui.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.updateCmd()
        self.start_pushBtn.clicked.connect(self.start)
        self.width_spinBox.valueChanged.connect(self.updateCmd)
        self.height_spinBox.valueChanged.connect(self.updateCmd)
        self.food_spinBox.valueChanged.connect(self.updateCmd)
        self.bricks_spinBox.valueChanged.connect(self.updateCmd)
        self.worldFile_radioBtn.clicked.connect(self.updateCmd)
        self.randomWorld_radioBtn.clicked.connect(self.updateCmd)
        self.pathToExe_lineEd.textChanged.connect(self.updateCmd)
        self.snakeLength_spinBox.valueChanged.connect(self.updateCmd)
        self.gameSpeed_spinBox.valueChanged.connect(self.updateCmd)
        self.worldFilename_lineEd.textChanged.connect

    def start(self):
        cmd = str(self.command_lineEd.text()).split()
        Popen(cmd, bufsize=-1)
        self.close()

    def updateCmd(self):
        if bool(self.randomWorld_radioBtn.isChecked()):
            print('a')
            self.randomWorld_frame.setEnabled(True)
            self.fileWorld_frame.setEnabled(False)
            widht = self.width_spinBox.value()
            heigth = self.height_spinBox.value()
            food = self.food_spinBox.value()
            bricks = self.bricks_spinBox.value()
            world = '{widht} {heigth} {food} {bricks}'.format(
                widht=widht, heigth=heigth, food=food, bricks=bricks)
        elif bool(self.worldFile_radioBtn.isChecked()):
            print('b')
            self.randomWorld_frame.setEnabled(False)
            self.fileWorld_frame.setEnabled(True)
            world = self.worldFilename_lineEd.text()
        exe = self.pathToExe_lineEd.text()
        length = self.snakeLength_spinBox.value()
        speed = self.gameSpeed_spinBox.value()
        cmd = '{exe} {len} {speed} {world}'.format(exe=exe, len=length, speed=speed, world=world)
        self.command_lineEd.setText(cmd)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    myapp.show()
    sys.exit(app.exec_())
