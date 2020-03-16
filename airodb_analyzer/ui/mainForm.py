from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.openSessionForm import Ui_OpenSessionForm
from ui.aboutBoxForm import Ui_AboutBoxForm
from ui.manageTrustedAPsForm import Ui_ManageTrustedAPsForm
from services.dbStorage import DBStorage
from models.accessPoint import AccessPoint
from models.macAddress import MACAddress
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
        self.toggleControlsForSession(False)
        #Signals
        self.tabWidgetAPDetails.currentChanged.connect(self.APDetailsTabChanged)
        self.action_Quit.triggered.connect(self.menuQuitClick)
        self.action_Open_session.triggered.connect(self.menuOpenSessionClick)
        self.actionClose_session.triggered.connect(self.menuCloseSessionClick)
        self.action_Open_session_toolbar.triggered.connect(self.menuOpenSessionClick)
        self.action_Close_session_toolbar.triggered.connect(self.menuCloseSessionClick)
        self.action_Show_all_APs.triggered.connect(self.menuShowAllClick)
        self.action_Show_trusted_APs.triggered.connect(self.toggleMenusShowAPsClick)
        self.action_Show_untrusted_APs.triggered.connect(self.toggleMenusShowAPsClick)
        self.action_Show_hidden_APs.triggered.connect(self.toggleMenusShowAPsClick)
        self.action_Manage_Trusted_access_points.triggered.connect(self.menuManageTrustedAPsClick)
        self.action_ManageKnownAccessPoints_toolbar.triggered.connect(self.menuManageTrustedAPsClick)
        self.actionAbout_airodb_analyzer.triggered.connect(self.menuAboutBoxClick)
        self.listViewAP.selectionModel().selectionChanged.connect(self.listViewAPCurrentChange)
        self.buttonAddToTrustedAP.clicked.connect(self.buttonAddToTrustedAPClick)
        self.buttonRemoveFromTrustedAP.clicked.connect(self.buttonRemoveFromTrustedAPClick)
        self.showMaximized()

    def showEvent(self, event):
        QtCore.QTimer.singleShot(200, lambda: self.lineEditFilterAPs.setStyleSheet("#lineEditFilterAPs { color: lightGray; }"))

    def menuQuitClick(self):
        self.close()

    def menuAboutBoxClick(self):
        formAboutBox = Ui_AboutBoxForm()
        formAboutBox.exec_()

    def loadSession(self, sessionName):
        storage = DBStorage()
        apList = storage.getSessionAP(sessionName)
        self.loadTrustedAPs()
        self._sessionName = sessionName
        self.apListModel.clear()
        self.apListMACAddress.clear()
        for ap in apList:
            apDisplayName = ap.getName()
            if (ap.isHidden()):
                apDisplayName = "<hidden>"
            if ((not(self.action_Show_hidden_APs.isChecked()) and ap.isHidden())
                or (not(self.action_Show_trusted_APs.isChecked()) and ap.isTrusted(self._trustedAPList))
                or (not(self.action_Show_untrusted_APs.isChecked()) and not(ap.isTrusted(self._trustedAPList)))):
                pass
            else:
                item = QtGui.QStandardItem(apDisplayName)
                self.apListModel.appendRow(item)
                self.apListMACAddress.append(ap.getMACAddress())

        self.tabWidgetAPDetails.setVisible(False)
        self.toggleControlsForSession(True)

    def loadTrustedAPs(self):
        storage = DBStorage()
        self._trustedAPList = storage.getTrustedAPList()

    def closeSession(self):
        self._sessionName = ""
        self.apListModel.clear()
        self.apListMACAddress = []
        self.tabWidgetAPDetails.setVisible(False)
        self.toggleControlsForSession(False)

    def toggleControlsForSession(self, isSessionOpen):
        self.action_Close_session_toolbar.setEnabled(isSessionOpen)
        self.actionClose_session.setEnabled(isSessionOpen)
        self.action_Show_hidden_APs.setEnabled(isSessionOpen)

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
                self.loadAPRawLogs(self._sessionName, apMACAddress.getValue())

    def listViewAPCurrentChange(self):
        apMACAddress = self.getSelectedAPMACAddress()
        if (apMACAddress != None):
            storage = DBStorage()
            apStat = storage.getSessionAPStats(self._sessionName, apMACAddress)
            if (apStat != None):
                ap = AccessPoint(apStat.getMACAddress(), apStat.getName())
                self.labelName.setText(apStat.getName())
                self.labelMACAddress.setText(apStat.getMACAddress().getValue())
                isTrustedAP = ap.isTrusted(self._trustedAPList)
                self.buttonAddToTrustedAP.setVisible(not(isTrustedAP))
                self.buttonRemoveFromTrustedAP.setVisible(isTrustedAP)
                self.labelFirstTimeSeen.setText(str(apStat.getFirstTimeSeen()))
                self.labelLastTimeSeen.setText(str(apStat.getLastTimeSeen()))
                self.widgetProtectionDetails.setVisible(apStat.isProtected())
                self.labelIsProtected.setText("True" if apStat.isProtected() else "False")
                self.labelEncryption.setText(apStat.getEncryption())
                self.labelCipher.setText(apStat.getCipher())
                self.labelAuthentification.setText(apStat.getAuthentification())
                self.labelChannel.setText(str(apStat.getChannel()))
                self.labelSpeed.setText(str(apStat.getSpeed()))
                self.labelPowerMin.setText(str(apStat.getPowerLevelMax())) #Max for best signal
                self.labelPowerMax.setText(str(apStat.getPowerLevelMin())) #Min for worst signal
                self.labelPowerAvg.setText(str(apStat.getPowerLevelAvg()))
                self.tabWidgetAPDetails.setCurrentIndex(0)
                self.tabWidgetAPDetails.setVisible(True)

    def menuShowAllClick(self):
        self.action_Show_trusted_APs.setChecked(True)
        self.action_Show_untrusted_APs.setChecked(True)
        self.action_Show_hidden_APs.setChecked(True)
        self.loadSession(self._sessionName)

    def toggleMenusShowAPsClick(self):
        self.loadSession(self._sessionName)

    def menuManageTrustedAPsClick(self):
        formManageTrustedAPs = Ui_ManageTrustedAPsForm()
        formManageTrustedAPs.exec_()
        self.loadTrustedAPs()
    
    def buttonAddToTrustedAPClick(self):
        storage = DBStorage()
        self.updateFromTrustedAPList(storage.insertTrustedAP)

    def buttonRemoveFromTrustedAPClick(self):
        storage = DBStorage()
        self.updateFromTrustedAPList(storage.deleteTrustedAP)

    def updateFromTrustedAPList(self, func):
        apMACAddress = self.getSelectedAPMACAddress()
        if (apMACAddress != None):
            storage = DBStorage()
            func(apMACAddress)
            self.loadTrustedAPs()
            ap = AccessPoint(apMACAddress, "")
            isTrustedAP = ap.isTrusted(self._trustedAPList)
            self.buttonAddToTrustedAP.setVisible(not(isTrustedAP))
            self.buttonRemoveFromTrustedAP.setVisible(isTrustedAP)
