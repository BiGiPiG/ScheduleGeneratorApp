from PyQt6.QtGui import QPalette, QColor, QTextCharFormat
from PyQt6.QtWidgets import QComboBox, QCalendarWidget, QStyledItemDelegate
from PyQt6.QtCore import Qt, QDate, QEvent, pyqtSignal
from PyQt6 import QtGui


class CalendarComboBox(QComboBox):
    dateClicked = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setWindowFlags(Qt.WindowType.Popup)
        self.calendar.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.calendar.clicked.connect(self._date_selected)

        self.enabled_dates = list()
        self.disable_all_dates()

        # Формат для активных дат
        self.enabled_format = QTextCharFormat()
        self.enabled_format.setForeground(QColor("#000000"))
        self.enabled_format.setBackground(QColor("#E6E0FF"))

        # Стандартное отображение
        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QColor("#000000"))  # Черный цвет для текста
        self.default_format.setBackground(QColor("#ffffff"))  # Белый фон

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))  # Цвет текста
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#000000"))  # Цвет плейсхолдера
        self.setPalette(palette)

        # Стили календаря
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                font-size: 12px;
                border: 1px solid #9187E5;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #9187E5;
            }   
            QCalendarWidget QToolButton {
                font-size: 14px;
                color: white;
                background-color: #9187E5;
                border: none;
                padding: 5px;
            }
            QCalendarWidget QAbstractItemView::item:selected {
                background-color: #9187E5;
                color: white; 
            }
        """)

        self.setStyleSheet("""
            QComboBox {
                font-family: 'Inter';
                font-size: 24px;
                color: #000000;
            }
        """)

        # Убираем стандартный выпадающий список
        self.setItemDelegate(QStyledItemDelegate())


        palette = self.lineEdit().palette()
        palette.setColor(QtGui.QPalette.ColorRole.PlaceholderText, QtGui.QColor("#000000"))
        self.lineEdit().setPalette(palette)

    def disable_all_dates(self):
        """Делает все даты в календаре неактивными"""
        disabled_format = QTextCharFormat()
        disabled_format.setForeground(QColor("#cccccc"))
        disabled_format.setBackground(QColor("#f0f0f0"))

        # Применяем формат ко всем датам
        for year in range(1900, 2100):
            for month in range(1, 13):
                for day in range(1, 32):
                    try:
                        date = QDate(year, month, day)
                        self.calendar.setDateTextFormat(date, self.default_format)
                    except:
                        pass
        self.lineEdit().clear()
        self.lineEdit().setPlaceholderText("Выберите дату")

    def showPopup(self):
        """Переопределяем метод показа popup"""
        if not self.calendar.isVisible():
            pos = self.mapToGlobal(self.rect().bottomLeft())
            self.calendar.move(pos)
            self.calendar.show()

    def hidePopup(self):
        """Переопределяем метод скрытия popup"""
        self.calendar.hide()

    def _date_selected(self, date):
        if date not in self.enabled_dates:
            return

        date_str = date.toString("yyyy-MM-dd")
        self.lineEdit().setText(date_str)
        self.hidePopup()
        self.dateClicked.emit(date)

    def event(self, e):
        """Обработка событий для закрытия календаря"""
        if e.type() == QEvent.Type.Close:
            self.hidePopup()
        return super().event(e)

    def set_enabled(self, flag):
        self.setEnabled(flag)

    def set_enabled_dates(self, enabled_dates):
        self.enabled_dates = set()
        self.disable_all_dates()

        for date_str in enabled_dates:
            q_date = QDate.fromString(date_str, "yyyy-MM-dd")
            self.enabled_dates.add(q_date)
            self.calendar.setDateTextFormat(q_date, self.enabled_format)

