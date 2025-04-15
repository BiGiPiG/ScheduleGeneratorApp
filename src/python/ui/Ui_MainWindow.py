from PyQt6 import QtWidgets

from src.python.ui.components.left_panel import LeftPanel
from src.python.ui.components.right_panel import RightPanel


class Ui_MainWindow(object):
    def __init__(self):
        self.central_widget = None
        self.leftPanel = None

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(1000, 700)

        # Центральный виджет
        self.central_widget = QtWidgets.QWidget(parent=MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("background: #DCD9F1;")

        self.rightPanel = RightPanel(self.central_widget)

        # Левая панель
        self.leftPanel = LeftPanel(self.central_widget, self.rightPanel)

        # Установка центрального виджета
        MainWindow.setCentralWidget(self.central_widget)
