from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal, Qt


class MultiSelectComboBox(QtWidgets.QComboBox):
    activated = pyqtSignal(list)

    def __init__(self, parent=None, geometry=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


        if geometry:
            self.setGeometry(geometry)

        self.setStyleSheet("""
            font-family: 'Inter';
            font-style: normal;
            font-weight: 300;
            font-size: 24px;
            line-height: 29px;
            color: #000000;
        """)

        self.lineEdit().setPlaceholderText("Выберите группы")

        palette = self.lineEdit().palette()
        palette.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor("#000000"))
        self.lineEdit().setPalette(palette)

        self.view().pressed.connect(self.handle_item_pressed)
        self._items = []
        self._prevent_hide = False

    def showPopup(self):
        self._prevent_hide = True
        super().showPopup()

    def hidePopup(self):
        if self._prevent_hide:
            self._prevent_hide = False
            return  # Блокируем закрытие при клике
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

        # Обновляем отображаемый текст
        self.updateDisplayText()

        self.activated.emit(self.selectedItems())
        self._prevent_hide = True

    def updateDisplayText(self):
        self.lineEdit().clear()
        self.lineEdit().setPlaceholderText("Выберите группы")

    def selectedItems(self):
        selected = []
        for i in range(self.count()):
            index = self.model().index(i, 0)
            if self.model().data(index, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked:
                selected.append(self.itemText(i))
        return selected

