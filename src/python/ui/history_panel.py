from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QFrame

from src.python.core.service_manager import ServiceManager


class HistoryPanel(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_table = None
        self.back_button = None
        self.title_label = None
        self.dbManager = ServiceManager()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(QtCore.QRect(10, 20, 980, 660))
        self.setObjectName("history_frame")
        self.setStyleSheet("""
            background: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 20px;
        """)

        # Заголовок
        self.title_label = QtWidgets.QLabel("История изменений", self)
        self.title_label.setStyleSheet("""
            border: none;
            outline: none;
            font-family: 'Inter';
            font-weight: 900;
            font-size: 32px;
            color: #000000;
        """)
        self.title_label.adjustSize()  # Авторасчёт размера по содержимому
        label_width = self.title_label.width()
        frame_width = self.width()
        self.title_label.setGeometry(
            (frame_width - label_width) // 2 + 25, 10, label_width, 40
        )
        self.title_label.setStyleSheet("""
            border: None;
            background: #FFFFFF;
            font-family: 'Inter';
            font-style: normal;
            font-weight: 900;
            font-size: 32px;
            line-height: 39px;
            display: flex;
            align-items: center;
            text-align: center;
            color: #000000;
        """)

        # Таблица истории
        table_width = 700
        table_height = 540
        table_x = (self.width() - table_width) // 2
        table_y = 70
        self.history_table = QtWidgets.QTableWidget(self)
        self.history_table.setFrameShape(QFrame.Shape.NoFrame)
        self.history_table.setGeometry(QtCore.QRect(table_x, table_y, table_width, table_height))
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Дата", "Действие", "Описание"])

        # Настройки отображения
        self.history_table.verticalHeader().setVisible(False)
        visible_height = 7 * 60 + self.history_table.horizontalHeader().height()
        self.history_table.setMaximumHeight(visible_height)
        self.history_table.setMinimumHeight(visible_height)

        # Настройки ресайза столбцов
        self.history_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.history_table.verticalHeader().setDefaultSectionSize(40)  # Стандартная высота
        self.history_table.verticalHeader().setMinimumSectionSize(30)  # Минимальная высота
        self.history_table.verticalHeader().setMaximumSectionSize(60)

        # Остальные настройки таблицы
        self.history_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.history_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.history_table.setStyleSheet("""
        
            QTableWidget {
                border: none;
                background-color: #FFFFFF;
                outline: none;
                gridline-color: transparent;
            }

            QHeaderView::section {
                background-color: #9187E5;
                color: white;
                font-weight: bold;
                padding: 8px;
                font-size: 12px;
                border: none;
                border-left: none;
                border-right: none;
                border-top: none;
                border-bottom: none;
                outline: none;
            }
            
            QHeaderView {
                border: none;
                outline: none;
            }

            QTableWidget::item {
                white-space: pre-wrap;
                border: none;
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #D1C4E9;
                color: black;
            }

            QTableWidget::item:focus {
                border: none;
                outline: none;
            }

            QTableWidget {
                show-decoration-selected: 1;
            }
        """)

        self.back_button = QtWidgets.QPushButton(self)
        self.back_button.setGeometry(QtCore.QRect(self.width() // 2 - 60, self.height() - 60, 150, 40),)
        self.back_button.setObjectName("back_button")
        self.back_button.setStyleSheet("""
                QPushButton {
                    font-family: 'Inter';
                    font-weight: 700;
                    font-size: 16px;
                    background-color: #9187E5;
                    color: white;
                    border-radius: 10px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #A99EFF;
                    border: 2px solid #FFFFFF;
                }
            """)
        self.back_button.setText("Назад")

    def show(self):
        super().show()

    def update_table(self):
        try:
            records = self.dbManager.info_service.get_all()[::-1]
            print(f"Получено записей: {len(records)}")

            self.history_table.setRowCount(len(records))

            for row_idx, record in enumerate(records):
                action = "Удаление" if record.action == 1 else "Перенос"

                date_item = QtWidgets.QTableWidgetItem(record.date)
                action_item = QtWidgets.QTableWidgetItem(action)
                desc_item = QtWidgets.QTableWidgetItem(record.description)

                for item in [date_item, action_item, desc_item]:
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable)

                self.history_table.setItem(row_idx, 0, date_item)
                self.history_table.setItem(row_idx, 1, action_item)
                self.history_table.setItem(row_idx, 2, desc_item)

                self.history_table.resizeRowToContents(row_idx)

            self.history_table.viewport().update()

        except Exception as e:
            print(f"Ошибка при обновлении таблицы: {e}")

