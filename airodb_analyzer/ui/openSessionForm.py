import operator
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class Ui_OpenSessionForm(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_OpenSessionForm, self).__init__()
        uic.loadUi('airodb_analyzer/designer/openSessionForm.ui', self)

        #Signals

    def showEvent(self, event):
        self.loadSessions()

    def loadSessions(self):
        self.tabledata=[[1,2,3,4],[5,6,7,8]]
        header = ['date', 'time', '', 'size', 'filename']
        tm = SessionModel(self.tabledata, header, self.tableView) 
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