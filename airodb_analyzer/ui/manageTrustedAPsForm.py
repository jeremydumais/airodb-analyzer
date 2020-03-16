from PyQt5 import QtCore, QtGui, QtWidgets, uic
from models.macAddress import MACAddress
from services.dbStorage import DBStorage
import qdarkgraystyle

class Ui_ManageTrustedAPsForm(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_ManageTrustedAPsForm, self).__init__()
        uic.loadUi('airodb_analyzer/designer/manageTrustedAPsForm.ui', self)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.apListModel = QtGui.QStandardItemModel(self.listViewTrustedAP)
        self.listViewTrustedAP.setModel(self.apListModel)
        self.frameAPDetail.setVisible(False)
        self.toggleListActionButton(False)
        #Icons
        self.buttonOK.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogOkButton))
        self.buttonCancel.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #Signals
        #self.lineEditMACAddress.returnPressed.connect(self.buttonOKClick)
        self.buttonClose.clicked.connect(self.buttonCloseClick)
        self.buttonOK.clicked.connect(self.buttonOKClick)
        self.buttonCancel.clicked.connect(self.buttonCancelClick)
        self.buttonAdd.clicked.connect(self.buttonAddClick)
        self.buttonUpdate.clicked.connect(self.buttonUpdateClick)
        self.buttonDelete.clicked.connect(self.buttonDeleteClick)
        self.listViewTrustedAP.selectionModel().selectionChanged.connect(self.listViewTrustedAPCurrentChange)
        self.listViewTrustedAP.mouseDoubleClickEvent = self.buttonUpdateClick
    
    def showEvent(self, event):
        self.loadTrustedAPs()

    def buttonCloseClick(self):
        self.close()

    def loadTrustedAPs(self):
        storage = DBStorage()
        apList = storage.getTrustedAPList()
        self.apListModel.clear()
        for ap in apList:
            item = QtGui.QStandardItem(ap.getValue())
            self.apListModel.appendRow(item)
        self.toggleListActionButton(False)

    def buttonOKClick(self):
        storage = DBStorage()
        macAddress = self.lineEditMACAddress.text().strip()
        if (macAddress==""):
            self.showInfo("The MAC Address field cannot be empty.")
            return
        try:
            MACAddress(macAddress)
        except:
            self.showError("The MAC Address value is invalid.(Ex. 01:23:34:56:78:9a)")
            return
        try:
            if (self._isInsertMode == True):
                storage.insertTrustedAP(MACAddress(macAddress))
            else:
                selectedAP = self.getSelectedAPMACAddress()
                if (selectedAP != None):
                    storage.updateTrustedAP(MACAddress(selectedAP), MACAddress(macAddress))
                else:
                    return
            self.loadTrustedAPs()
            self.frameAPDetail.setVisible(False)
            self.listViewTrustedAP.setEnabled(True)
        except Exception as e:
            self.showError(str(e))

    def buttonCancelClick(self):
        self.frameAPDetail.setVisible(False)
        self.listViewTrustedAP.setEnabled(True)

    def buttonAddClick(self):
        self._isInsertMode = True
        self.lineEditMACAddress.setText("")
        self.listViewTrustedAP.setEnabled(False)
        self.frameAPDetail.setVisible(True)
        self.lineEditMACAddress.setFocus()

    def buttonUpdateClick(self, event):
        selectedAP = self.getSelectedAPMACAddress()
        if (selectedAP != None):
            self._isInsertMode = False
            self.lineEditMACAddress.setText(selectedAP)
            self.listViewTrustedAP.setEnabled(False)
            self.frameAPDetail.setVisible(True)
            self.lineEditMACAddress.setFocus()

    def buttonDeleteClick(self):
        selectedAP = self.getSelectedAPMACAddress()
        if (selectedAP != None):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Are you sure you want to delete the AP " + selectedAP + "?")
            msg.setWindowTitle("Confirmation")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            retVal = msg.exec_()
            if (retVal == QtWidgets.QMessageBox.Yes):
                storage = DBStorage()
                storage.deleteTrustedAP(MACAddress(selectedAP))
                self.loadTrustedAPs()      

    def listViewTrustedAPCurrentChange(self):
        selectedAP = self.getSelectedAPMACAddress()
        if (selectedAP != None):
            self.toggleListActionButton(True)
        else:
            self.toggleListActionButton(False)

    def getSelectedAPMACAddress(self):
        selectedRows = self.listViewTrustedAP.selectionModel().selectedRows()
        if (len(selectedRows) > 0):
            return selectedRows[0].data()
        else:
            return None

    def toggleListActionButton(self, isEnabled):
        self.buttonUpdate.setEnabled(isEnabled)
        self.buttonDelete.setEnabled(isEnabled)

    def showInfo(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Information")
        msg.exec_()

    def showError(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()