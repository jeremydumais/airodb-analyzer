from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qdarkgraystyle

class Ui_ManageTrustedAPsForm(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_ManageTrustedAPsForm, self).__init__()
        uic.loadUi('airodb_analyzer/designer/manageTrustedAPsForm.ui', self)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        self.frameAPDetail.setVisible(False)
        #Icons
        self.buttonOK.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogOkButton))
        self.buttonCancel.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        #Signals
        self.buttonClose.clicked.connect(self.buttonCloseClick)
    
    def buttonCloseClick(self):
        self.close()