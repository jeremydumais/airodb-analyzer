from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui.mainForm import Ui_MainWindow

if __name__ == '__main__':
    import sys
    import os
    import qdarkgraystyle

    # set the environment variable to use a specific wrapper
    # it can be set to pyqt, pyqt5, pyside or pyside2 (not implemented yet)
    # you do not need to use QtPy to set this variable
    os.environ['QT_API'] = 'pyqt5'

    app = QtWidgets.QApplication(sys.argv)
    mainForm = Ui_MainWindow()
    # setup stylesheet
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    sys.exit(app.exec_())
