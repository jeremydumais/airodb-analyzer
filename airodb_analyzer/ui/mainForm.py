from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.openSessionForm import Ui_OpenSessionForm
from services.dbStorage import DBStorage

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('airodb_analyzer/designer/mainForm.ui', self)
        self.apListModel = QtGui.QStandardItemModel(self.listViewAP)
        self.apListMACAddress = []
        self.listViewAP.setModel(self.apListModel)
        #Signals
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)
        self.listViewAP.selectionModel().selectionChanged.connect(self.listViewAPCurrentChange)

        self.show()

    def showEvent(self, event):
        #pass
        self.menuOpenSessionClick()

    def menuQuitClick(self):
        self.close()

    def loadSession(self, sessionName):
        storage = DBStorage()
        apList = storage.getSessionAP(sessionName)
        self.apListModel.clear()
        self.apListMACAddress.clear()
        for ap in apList:
            item = QtGui.QStandardItem(ap['name'])
            self.apListModel.appendRow(item)
            self.apListMACAddress.append(ap["_id"])

    def menuOpenSessionClick(self):
        formOpenSession = Ui_OpenSessionForm()
        result = formOpenSession.exec_()
        if (result == QtWidgets.QDialog.Accepted):
            self.loadSession(formOpenSession.selectedSession)

    def listViewAPCurrentChange(self):
        index = self.listViewAP.selectionModel().selectedRows()
        if (len(index) > 0):
            row = index[0].row()
            index2 = self.apListModel.index(row,0)

            self.labelName.setText(self.apListModel.data(index2))
            self.labelMACAddress.setText(self.apListMACAddress[row])
        pass