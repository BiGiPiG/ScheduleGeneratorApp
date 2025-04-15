from PyQt6 import QtCore, QtWidgets

from src.python.core.database_manager import DatabaseManager
from src.python.ui.components.calendar_combo_box import CalendarComboBox
from src.python.ui.components.multiselect_combo_box import MultiSelectComboBox


def create_label(parent, geometry, text, object_name):
    """Создание метки с общими стилями"""
    label = QtWidgets.QLabel(parent=parent)
    label.setGeometry(geometry)
    label.setObjectName(object_name)
    label.setStyleSheet("""
        border: none;
        font-family: 'Inter';
        font-style: normal;
        font-weight: 700;
        font-size: 24px;
        line-height: 29px;
        display: flex;
        align-items: center;
        text-align: center;
        color: #000000;
    """)
    label.setText(text)
    return label


def create_button(parent, geometry, text, object_name):
    """Создание кнопки с общими стилями"""
    button = QtWidgets.QPushButton(parent=parent)
    button.setGeometry(geometry)
    button.setObjectName(object_name)
    button.setStyleSheet("""
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
    button.setText(text)
    return button


class LeftPanel(QtWidgets.QFrame):
    def __init__(self, parent=None, right_panel=None):
        super().__init__(parent)
        self.setup_ui(parent)
        self.right_panel = right_panel

        # подключение к бд
        self.dbManager = DatabaseManager()

        # инициализируем селеторы
        self.set_defaul_comboboxes()

    def setup_ui(self, parent):
        self.setGeometry(QtCore.QRect(10, 20, 485, 660))
        self.setObjectName("left_frame")
        self.setStyleSheet("""
            background: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 20px;
        """)

        # Компоненты
        self.setup_comboboxes()
        self.setup_buttons()
        self.setup_main_text()

    def setup_comboboxes(self):
        # Группа
        self.group_label = create_label(
            parent=self,
            geometry=QtCore.QRect(50, 80, 100, 30),
            text="Группа",
            object_name="group_label"
        )

        self.group_multiSelectComboBox = MultiSelectComboBox(parent=self,
                                                             geometry=QtCore.QRect(50, 110, 220, 30)
                                                             )

        # Дисциплина
        self.discipline_label = create_label(
            parent=self,
            geometry=QtCore.QRect(50, 150, 160, 30),
            text="Дисциплина",
            object_name="descipline"
        )
        self.discipline_comboBox = self.create_combobox(QtCore.QRect(50, 180, 240, 30), "Выберите предмет")

        # Дата
        self.date_label = create_label(
            parent=self,
            geometry=QtCore.QRect(50, 220, 100, 30),
            text="Дата",
            object_name="date"
        )
        self.date_comboBox = CalendarComboBox(self)
        self.date_comboBox.setGeometry(QtCore.QRect(50, 250, 200, 30))

        self.date_comboBox.dateClicked.connect(self.activate_choice_button)
        self.group_multiSelectComboBox.activated.connect(self.update_combo_boxes)
        self.discipline_comboBox.activated.connect(self.update_combo_boxes)

    def setup_buttons(self):
        parent_width = self.width()
        x_position = (parent_width - 150) // 2

        self.choice_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 410, 150, 40),
            text="Выбрать",
            object_name="choice_button"
        )
        self.history_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 480, 150, 40),
            text="История",
            object_name="history_button"
        )
        self.reset_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 550, 150, 40),
            text="Сбросить",
            object_name="reset_button"
        )

        self.reset_button.clicked.connect(self.set_defaul_comboboxes)
        self.choice_button.clicked.connect(self.update_right_panel)

    def create_combobox(self, geometry, placeholder):
        combo = QtWidgets.QComboBox(self)
        combo.setGeometry(geometry)
        combo.setPlaceholderText(placeholder)
        combo.setStyleSheet("""

            QComboBox {
                font-family: 'Inter';
                font-style: normal;
                font-weight: 300;
                font-size: 24px;
                line-height: 29px;
                color: #000000;
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
            
        """)
        return combo

    def setup_main_text(self):
        """Настройка основного заголовка"""
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setGeometry(QtCore.QRect(132, 10, 220, 40))
        self.main_text.setObjectName("main_text")
        self.main_text.setText("Выбор пары")
        self.main_text.setStyleSheet("""
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

    def update_group_multiSelector(self):

        if self.discipline_comboBox.currentIndex() == -1:
            self.group_multiSelectComboBox.updateItems(self.dbManager.group_service.get_all())
        else:
            self.group_multiSelectComboBox.updateItems(self.dbManager.group_service.get_by_discipline(
                self.discipline_comboBox.currentText()[:-3]
            ))

    def update_discipline_comboBox(self):
        # Блокируем сигналы для предотвращения рекурсивных обновлений
        self.discipline_comboBox.blockSignals(True)

        # Сохраняем текущий выбранный элемент
        current_selection = self.discipline_comboBox.currentText()

        self.discipline_comboBox.clear()

        try:
            if self.group_multiSelectComboBox.selectedItems():
                disciplines = self.dbManager.discipline_service.get_by_groups(
                    self.group_multiSelectComboBox.selectedItems()
                )
            else:
                disciplines = self.dbManager.discipline_service.get_all()

            discipline_names = [disc.title + " " + disc.worktype for disc in disciplines]

            self.discipline_comboBox.addItems(discipline_names)

            # Восстанавливаем предыдущий выбор, если он все еще доступен
            if current_selection in discipline_names:
                self.discipline_comboBox.setCurrentText(current_selection)

        except Exception as e:
            print(f"Ошибка при обновлении списка дисциплин: {e}")
        finally:
            # Всегда разблокируем сигналы
            self.discipline_comboBox.blockSignals(False)

    def update_date_comboBox(self):
        print(self.discipline_comboBox.currentText())
        if self.discipline_comboBox.currentIndex() != -1 and self.group_multiSelectComboBox.selectedItems():
            self.date_comboBox.set_enabled_dates(
                self.dbManager.date_service.get_by_discs_and_groups(
                    self.discipline_comboBox.currentText()[:-3],
                    self.discipline_comboBox.currentText()[-2:],
                    self.group_multiSelectComboBox.selectedItems()
                )
            )
            self.date_comboBox.setEnabled(True)
        else:
            self.date_comboBox.setEnabled(False)

    def update_combo_boxes(self):
        self.update_group_multiSelector()
        self.update_discipline_comboBox()
        self.update_date_comboBox()

    def set_defaul_comboboxes(self):
        group_placeholder = self.group_multiSelectComboBox.lineEdit().placeholderText()
        self.group_multiSelectComboBox.addItems(self.dbManager.group_service.get_all())
        self.group_multiSelectComboBox.lineEdit().clear()
        self.group_multiSelectComboBox.lineEdit().setPlaceholderText(group_placeholder)

        self.discipline_comboBox.clear()
        self.discipline_comboBox.addItems(
            disc.title + " " + disc.worktype for disc in self.dbManager.discipline_service.get_all())

        self.date_comboBox.disable_all_dates()
        self.date_comboBox.setEnabled(False)
        self.choice_button.setEnabled(False)

    def activate_choice_button(self):
        self.choice_button.setEnabled(True)

    def update_right_panel(self):
        discipline = self.dbManager.discipline_service.get_all_discipline_information(
            self.group_multiSelectComboBox.selectedItems(),
            self.date_comboBox.currentText(),
            self.discipline_comboBox.currentText()[:-3],
            self.discipline_comboBox.currentText()[-2:]
        )

        prep = self.dbManager.discipline_service.get_prep(
            self.group_multiSelectComboBox.selectedItems(),
            self.date_comboBox.currentText(),
            self.discipline_comboBox.currentText()[:-3],
            self.discipline_comboBox.currentText()[-2:]
        )

        if not prep:
            prep = "Неизвестно"
        else:
            prep = prep[0]

        self.right_panel.update_selected_groups(self.group_multiSelectComboBox.selectedItems())
        self.right_panel.update_labels(discipline, prep)
