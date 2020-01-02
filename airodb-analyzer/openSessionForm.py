import operator
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OpenSessionForm(object):
    def setupUi(self, OpenSessionForm):
        OpenSessionForm.setObjectName("OpenSessionForm")
        OpenSessionForm.resize(400, 300)
        OpenSessionForm.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(OpenSessionForm)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtWidgets.QTableView(OpenSessionForm)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(OpenSessionForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(OpenSessionForm)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(OpenSessionForm)
        self.buttonBox.accepted.connect(OpenSessionForm.accept)
        self.buttonBox.rejected.connect(OpenSessionForm.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenSessionForm)

        #
        self.loadSessions()

    def retranslateUi(self, OpenSessionForm):
        _translate = QtCore.QCoreApplication.translate
        OpenSessionForm.setWindowTitle(_translate("OpenSessionForm", "Open a session"))
        self.label.setText(_translate("OpenSessionForm", "Select the session to open:"))

    def loadSessions(self):
        self.tabledata=[[1,2,3,4],[5,6,7,8]]
        header = ['date', 'time', '', 'size', 'filename']
        tm = SessionModel(self.tabledata, header, self.tableView) 
        self.tableView.setModel(tm)
        self.tableView.setSortingEnabled(True)

class SessionModel(QtCore.QAbstractTableModel): 
    def __init__(self, data, headerdata, parent=None, *args): 
        """ data: a list of lists
            headerdata: a list of strings
        """
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
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        #self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()")) 
        reverse = False 
        if order == QtCore.Qt.DescendingOrder: 
            reverse = True 
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol), reverse=reverse) 
        #self.emit(QtCore.SIGNAL("layoutChanged()"))
        self.layoutChanged.emit()