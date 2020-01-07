from PyQt5 import QtCore, QtGui, QtWidgets, uic
import qdarkgraystyle

class Ui_AboutBoxForm(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_AboutBoxForm, self).__init__()
        uic.loadUi('airodb_analyzer/designer/aboutBoxForm.ui', self)
        self.setStyleSheet(qdarkgraystyle.load_stylesheet())
        #Signals
        self.buttonClose.clicked.connect(self.buttonCloseClick)
    
    def buttonCloseClick(self):
        self.close()