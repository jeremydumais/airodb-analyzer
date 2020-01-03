from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.openSessionForm import Ui_OpenSessionForm

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('airodb_analyzer/designer/mainForm.ui', self)
        self.show()

        #Signals
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)

    def showEvent(self, event):
        self.menuOpenSessionClick()

    def menuQuitClick(self):
        self.close()

    def menuOpenSessionClick(self):
        formOpenSession = Ui_OpenSessionForm()
        result = formOpenSession.exec_()
        #if (result == QtWidgets.QDialog.Accepted):
        #    self.close()
