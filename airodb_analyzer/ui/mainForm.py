from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.openSessionForm import Ui_OpenSessionForm
from services.dbStorage import DBStorage

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('airodb_analyzer/designer/mainForm.ui', self)
        self.tabWidgetAPDetails.setVisible(False)
        self._sessionName = ""
        self.apListModel = QtGui.QStandardItemModel(self.listViewAP)
        self.apListMACAddress = []
        self.listViewAP.setModel(self.apListModel)
        #Signals
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)
        self.action_Open_session_toolbar.triggered.connect(self.menuOpenSessionClick)
        self.listViewAP.selectionModel().selectionChanged.connect(self.listViewAPCurrentChange)

        self.show()

    def showEvent(self, event):
        pass
        #self.menuOpenSessionClick()

    def menuQuitClick(self):
        self.close()

    def loadSession(self, sessionName):
        storage = DBStorage()
        apList = storage.getSessionAP(sessionName)
        self._sessionName = sessionName
        self.apListModel.clear()
        self.apListMACAddress.clear()
        for ap in apList:
            item = QtGui.QStandardItem(ap['name'])
            self.apListModel.appendRow(item)
            self.apListMACAddress.append(ap["_id"])
        self.tabWidgetAPDetails.setVisible(False)
        
    def menuOpenSessionClick(self):
        formOpenSession = Ui_OpenSessionForm()
        result = formOpenSession.exec_()
        if (result == QtWidgets.QDialog.Accepted):
            self.loadSession(formOpenSession.selectedSession)

    def listViewAPCurrentChange(self):
        selectedRows = self.listViewAP.selectionModel().selectedRows()
        if (len(selectedRows) > 0):
            row = selectedRows[0].row()
            apMACAddress = self.apListMACAddress[row]
            storage = DBStorage()
            apStats = storage.getSessionAPStats(self._sessionName, apMACAddress)
            record = apStats.next()
            isProtected = (record["Encryption"] != "OPN")
            self.labelName.setText(record["name"])
            self.labelMACAddress.setText(apMACAddress)
            self.labelFirstTimeSeen.setText(record["FirstTimeSeen"])
            self.labelLastTimeSeen.setText(record["LastTimeSeen"])
            self.widgetProtectionDetails.setVisible(isProtected)
            self.labelIsProtected.setText("True" if isProtected else "False")
            self.labelEncryption.setText(record["Encryption"])
            self.labelCipher.setText(record["Cipher"])
            self.labelAuthentification.setText(record["Authentification"])
            self.labelChannel.setText(str(record["Channel"]))
            self.labelSpeed.setText(str(record["Speed"]))
            self.tabWidgetAPDetails.setVisible(True)