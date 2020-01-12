import operator
from pymongo import MongoClient
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from services.dbStorage import DBStorage
import qdarkgraystyle

class Ui_OpenSessionForm(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_OpenSessionForm, self).__init__()
        uic.loadUi('airodb_analyzer/designer/openSessionForm.ui', self)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        #Icons
        self.buttonOK.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogOkButton))
        self.buttonCancel.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #Signals
        self.buttonOK.clicked.connect(self.buttonOKClick)
        self.buttonCancel.clicked.connect(self.buttonCancelClick)

    def showEvent(self, event):
        self.loadSessions()
    
    def buttonOKClick(self):
        index = self.tableView.selectionModel().selectedRows()
        if (len(index) > 0):
            self.selectedSession = index[0].data()
            self.accept()

    def buttonCancelClick(self):
        self.reject()

    def loadSessions(self):
        storage = DBStorage()
        sessions = storage.getSessionList()  
        listContent = []     
        for session in sessions:
            listContent.append([session.getName(), 
                str(session.getFirstEntryDateTime()),
                str(session.getLastEntryDateTime()),
                session.getNBOfRawLogs()])
        header = ['Session Name', 'First entry', 'Last entry', 'Number of entries']
        tm = SessionModel(listContent, header, self.tableView) 
        self.tableView.setModel(tm)
        self.tableView.setSortingEnabled(True)

class SessionModel(QtCore.QAbstractTableModel): 
    def __init__(self, data, headerdata, parent=None, *args): 
        QtCore.QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = data
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QtCore.QVariant() 
        elif role != QtCore.Qt.DisplayRole: 
            return QtCore.QVariant() 
        return QtCore.QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()

    def sort(self, Ncol, order):
        self.layoutAboutToBeChanged.emit()
        reverse = False 
        if order == QtCore.Qt.DescendingOrder: 
            reverse = True 
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol), reverse=reverse) 
        self.layoutChanged.emit()