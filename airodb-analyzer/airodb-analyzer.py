from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self._form = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Open_session = QtWidgets.QAction(MainWindow)
        self.action_Open_session.setObjectName("action_Open_session")
        self.menu_File.addAction(self.action_Open_session)
        self.menu_File.addAction(self.action_Quit)
        self.menu_File.triggered.connect(self.buttonQuitClick)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "airodb-analyzer"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.action_Open_session.setText(_translate("MainWindow", "&Open a session..."))

    def buttonQuitClick(self):
        self._form.close()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainForm = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainForm)
    mainForm.show()
    sys.exit(app.exec_())
