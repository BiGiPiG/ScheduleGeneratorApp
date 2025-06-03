from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal, Qt, QTimer


class MultiSelectComboBox(QtWidgets.QComboBox):
    activated = pyqtSignal(list)

    def __init__(self, parent=None, geometry=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lineEdit().installEventFilter(self)

        self.setFixedHeight(30)
        self.setMinimumWidth(240)
        if geometry:
            self.setGeometry(geometry)

        self.setStyleSheet("""
            QComboBox {
                font-family: 'Inter';
                font-style: normal;
                font-weight: 300;
                font-size: 24px;
                line-height: 29px;
                color: #808080;  /* Серый цвет текста */
                border-radius: 0px;
            }

            QComboBox QAbstractItemView {
                border-radius: 0px; 
            }

            QComboBox QAbstractItemView::item {
                border-radius: 0px;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #9187E5;
                color: #FFFFFF;       
            }

            QComboBox QLineEdit {
                color: #808080;  /* Серый цвет текста в поле ввода */
            }
        """)

        self.lineEdit().setPlaceholderText("Выберите группы")

        self.view().pressed.connect(self.handle_item_pressed)
        self._items = []

    def showPopup(self):
        super().showPopup()

    def hidePopup(self):
        super().hidePopup()

    def addItems(self, items):
        self.clear()
        self._items = items
        for item in items:
            self.addItem(item)
            index = self.model().index(self.count() - 1, 0)
            self.model().setData(index, Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        self.updateDisplayText()

    def updateItems(self, items):
        selected_items = self.selectedItems()
        self.clear()
        self._items = items
        for item in items:
            self.addItem(item)
            index = self.model().index(self.count() - 1, 0)
            self.model().setData(index, Qt.CheckState.Unchecked if item not in selected_items else Qt.CheckState.Checked,
                                 Qt.ItemDataRole.CheckStateRole)
        self.updateDisplayText()

    def handle_item_pressed(self, index):
        current_state = self.model().data(index, Qt.ItemDataRole.CheckStateRole)
        new_state = Qt.CheckState.Unchecked if current_state == Qt.CheckState.Checked else Qt.CheckState.Checked
        self.model().setData(index, new_state, Qt.ItemDataRole.CheckStateRole)

        self.updateDisplayText()
        self.activated.emit(self.selectedItems())

    def updateDisplayText(self):
        selected = self.selectedItems()
        trimmed = [item[-5:] for item in selected]
        text = " ".join(trimmed) if trimmed else "Выберите группы"
        self.lineEdit().blockSignals(True)
        self.lineEdit().setText(text)
        self.lineEdit().blockSignals(False)

    def selectedItems(self):
        selected = []
        for i in range(self.count()):
            index = self.model().index(i, 0)
            if self.model().data(index, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                selected.append(self.itemText(i))
        return selected

    def eventFilter(self, source, event):
        if source == self.lineEdit() and event.type() == event.Type.MouseButtonPress:
            QTimer.singleShot(100, self.forceShowPopup)
            return True
        return super().eventFilter(source, event)

    def forceShowPopup(self):
        self.setFocus()
        self.showPopup()