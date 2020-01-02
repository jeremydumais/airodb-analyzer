from PyQt5 import QtCore, QtGui, QtWidgets
from openSessionForm import Ui_OpenSessionForm

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self._form = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
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
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtWidgets.QListView(self.dockWidgetContents)
        self.listView.setResizeMode(QtWidgets.QListView.Fixed)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Open_session = QtWidgets.QAction(MainWindow)
        self.action_Open_session.setObjectName("action_Open_session")
        self.menu_File.addAction(self.action_Open_session)
        self.menu_File.addAction(self.action_Quit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Signals
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)
        #self.menuOpenSessionClick()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "airodb-analyzer"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "General"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Raw logs"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Discovered access points"))
        self.action_Quit.setText(_translate("MainWindow", "&Quit"))
        self.action_Open_session.setText(_translate("MainWindow", "&Open a session..."))

    def menuQuitClick(self):
        self._form.close()

    def menuOpenSessionClick(self):
        ui = QtWidgets.QDialog(self._form)
        formOpenSession = Ui_OpenSessionForm()
        formOpenSession.setupUi(ui)
        ui.exec_()

if __name__ == '__main__':
    import sys
    import os
    import qdarkstyle

    # set the environment variable to use a specific wrapper
    # it can be set to pyqt, pyqt5, pyside or pyside2 (not implemented yet)
    # you do not need to use QtPy to set this variable
    os.environ['QT_API'] = 'pyqt5'

    app = QtWidgets.QApplication(sys.argv)
    mainForm = QtWidgets.QMainWindow()

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())

    ui = Ui_MainWindow()
    ui.setupUi(mainForm)
    mainForm.show()
    sys.exit(app.exec_())
