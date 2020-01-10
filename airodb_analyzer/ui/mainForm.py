from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.openSessionForm import Ui_OpenSessionForm
from ui.aboutBoxForm import Ui_AboutBoxForm
from services.dbStorage import DBStorage
from bson.json_util import dumps

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        uic.loadUi('airodb_analyzer/designer/mainForm.ui', self)
        screenCenter = QtWidgets.QApplication.desktop().screen().rect().center()
        self.move(screenCenter.x()-self.width()/2, screenCenter.y()-self.height()/2);
        self.tabWidgetAPDetails.setVisible(False)
        self._sessionName = ""
        self.apListModel = QtGui.QStandardItemModel(self.listViewAP)
        self.apListMACAddress = []
        self.listViewAP.setModel(self.apListModel)
        #Signals
        self.tabWidgetAPDetails.currentChanged.connect(self.APDetailsTabChanged)
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)
        self.actionClose_session.triggered.connect(self.menuCloseSessionClick)
        self.action_Open_session_toolbar.triggered.connect(self.menuOpenSessionClick)
        self.action_Close_session_toolbar.triggered.connect(self.menuCloseSessionClick)
        self.actionAbout_airodb_analyzer.triggered.connect(self.menuAboutBoxClick)
        self.listViewAP.selectionModel().selectionChanged.connect(self.listViewAPCurrentChange)
        self.show()

    def showEvent(self, event):
        QtCore.QTimer.singleShot(200, lambda: self.lineEditFilterAPs.setStyleSheet("#lineEditFilterAPs { color: lightGray; }"))
        pass

    def menuQuitClick(self):
        self.close()

    def menuAboutBoxClick(self):
        formAboutBox = Ui_AboutBoxForm()
        formAboutBox.exec_()

    def loadSession(self, sessionName):
        storage = DBStorage()
        apList = storage.getSessionAP(sessionName)
        self._sessionName = sessionName
        self.apListModel.clear()
        self.apListMACAddress.clear()
        for ap in apList:
            apDisplayName = ap['name']
            if (apDisplayName == ""):
                apDisplayName = "<hidden>"
            item = QtGui.QStandardItem(apDisplayName)
            self.apListModel.appendRow(item)
            self.apListMACAddress.append(ap["_id"])
        self.tabWidgetAPDetails.setVisible(False)
        
    def closeSession(self):
        self._sessionName = ""
        self.apListModel.clear()
        self.apListMACAddress = []
        self.tabWidgetAPDetails.setVisible(False)

    def loadAPRawLogs(self, sessionName, apMACAddress):
        storage = DBStorage()
        logs = storage.getSessionAPRawLogs(sessionName, apMACAddress)
        rawLogs = ""
        for log in logs:
            rawLogs = rawLogs + dumps(log) + "\n"
        self.labelRawLogs.setText(rawLogs)

    def getSelectedAPMACAddress(self):
            selectedRows = self.listViewAP.selectionModel().selectedRows()
            if (len(selectedRows) > 0):
                row = selectedRows[0].row()
                return self.apListMACAddress[row]
            else:
                return None

    def menuOpenSessionClick(self):
        formOpenSession = Ui_OpenSessionForm()
        result = formOpenSession.exec_()
        if (result == QtWidgets.QDialog.Accepted):
            self.loadSession(formOpenSession.selectedSession)

    def menuCloseSessionClick(self):
        self.closeSession()

    def APDetailsTabChanged(self):
        if (self.tabWidgetAPDetails.currentIndex() == 1):
            apMACAddress = self.getSelectedAPMACAddress()
            if (apMACAddress != None):
                self.loadAPRawLogs(self._sessionName, apMACAddress)

    def listViewAPCurrentChange(self):
        apMACAddress = self.getSelectedAPMACAddress()
        if (apMACAddress != None):
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
            self.tabWidgetAPDetails.setCurrentIndex(0)
            self.tabWidgetAPDetails.setVisible(True)