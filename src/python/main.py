from PyQt6 import QtWidgets
import sys
from src.python.ui.Ui_MainWindow import Ui_MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec())
