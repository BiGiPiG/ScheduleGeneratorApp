from PyQt6 import QtWidgets

from src.python.ui.history_panel import HistoryPanel
from src.python.ui.left_panel import LeftPanel
from src.python.ui.right_panel import RightPanel


class Ui_MainWindow(object):
    def __init__(self):
        self.rightPanel = None
        self.central_widget = None
        self.leftPanel = None
        self.historyPanel = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(1000, 700)
        MainWindow.setWindowTitle("Reschedule Generator App")

        # Центральный виджет
        self.central_widget = QtWidgets.QWidget(parent=MainWindow)

        # Установка центрального виджета
        MainWindow.setCentralWidget(self.central_widget)

        self.rightPanel = RightPanel(self.central_widget)
        self.leftPanel = LeftPanel(self.central_widget)
        self.historyPanel = HistoryPanel(self.central_widget)

        self.show_main_panels()

        self.leftPanel.choice_button.clicked.connect(self.update_right_panel)
        self.leftPanel.history_button.clicked.connect(self.hide_panels)
        self.leftPanel.reset_button.clicked.connect(self.leftPanel.set_default_comboboxes)
        self.leftPanel.date_comboBox.dateClicked.connect(self.leftPanel.activate_choice_button)
        self.leftPanel.group_multiSelectComboBox.activated.connect(self.leftPanel.update_combo_boxes)
        self.leftPanel.discipline_comboBox.activated.connect(self.leftPanel.update_combo_boxes)
        self.leftPanel.reset_button.clicked.connect(self.rightPanel.set_default_labels)
        self.leftPanel.history_button.clicked.connect(self.historyPanel.update_table)


        self.rightPanel.cancel_button.clicked.connect(self.leftPanel.set_default_comboboxes)
        self.rightPanel.cancel_button.clicked.connect(self.rightPanel.show_cancel_dialog)
        self.rightPanel.reschedule_button.clicked.connect(self.rightPanel.show_reschedule_dialog)
        self.rightPanel.reschedule_button.clicked.connect(self.leftPanel.set_default_comboboxes)

        self.historyPanel.back_button.clicked.connect(self.show_main_panels)

        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("background: #DCD9F1;")

    def update_right_panel(self):
        discipline = self.leftPanel.dbManager.discipline_service.get_all_discipline_information(
            self.leftPanel.group_multiSelectComboBox.selectedItems(),
            self.leftPanel.date_comboBox.currentText(),
            self.leftPanel.discipline_comboBox.currentText()[:-3],
            self.leftPanel.discipline_comboBox.currentText()[-2:]
        )

        self.rightPanel.update_selected_groups(self.leftPanel.group_multiSelectComboBox.selectedItems())
        self.rightPanel.update_labels(discipline[0])

    def hide_panels(self):
        self.leftPanel.hide()
        self.rightPanel.hide()
        self.historyPanel.show()

    def show_main_panels(self):
        """Показывает основные панели и скрывает историю"""
        self.rightPanel.show()
        self.leftPanel.show()
        self.historyPanel.hide()