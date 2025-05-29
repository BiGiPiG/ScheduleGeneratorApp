from PyQt6 import QtCore, QtGui, QtWidgets

from src.core.service_manager import ServiceManager


def create_labeled_edit(parent, label_text, value_text, y, object_name):
    """Создание строки с лейблом и редактируемым полем"""
    label = QtWidgets.QLabel(parent)
    label.setGeometry(QtCore.QRect(50, y, 150, 30))
    label.setText(label_text)
    label.setStyleSheet("""
        font-family: 'Inter';
        font-weight: 600;
        font-size: 16px;
        color: #000000;
        border: none;
    """)

    line_edit = QtWidgets.QLineEdit(parent)
    line_edit.setGeometry(QtCore.QRect(210, y, 220, 30))
    line_edit.setObjectName(object_name)
    line_edit.setText(value_text)
    line_edit.setStyleSheet("""
        QLineEdit {
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 4px 8px;
            font-family: 'Inter';
            font-weight: 600;
            font-size: 16px;
            color: #000000;
        }
        QLineEdit:focus {
            border: 2px solid #9187E5;
        }
    """)

    return line_edit

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


class RightPanel(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_label = None
        self.setup_ui()
        self.dbManager = ServiceManager()

        self.selected_groups = list()
        self.old_date = None
        self.old_pair = None

    def setup_ui(self):
        self.setGeometry(QtCore.QRect(505, 20, 485, 660))
        self.setObjectName("right_frame")
        self.setStyleSheet("""
            background: #FFFFFF;
            border: 2px solid #000000;
            border-radius: 20px;
        """)

        self.setup_main_text()
        self.image_label = QtWidgets.QLabel(self)
        self.setup_image()
        self.setup_buttons()
        self.setup_labels()



    def setup_image(self):
        self.image_label.setStyleSheet("border: none;")
        self.image_label.setFixedSize(300, 300)
        self.image_label.move(
            (self.width() - 300) // 2,
            (self.height() - 300) // 2
        )

        try:
            pixmap = QtGui.QPixmap("../../images/Schedule.png")
            if pixmap.isNull():
                scaled_pixmap = pixmap.scaled(300, 300)
                self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")

    def setup_main_text(self):
        """Настройка основного заголовка"""
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setGeometry(QtCore.QRect(67, 10, 350, 40))  # Координаты относительно RightPanel
        self.main_text.setObjectName("main_text")
        self.main_text.setText("Редактор переноса")
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

    def setup_buttons(self):
        parent_width = self.width()
        x_position = (parent_width - 150) // 2

        self.reschedule_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 440, 150, 40),
            text="Перенести",
            object_name="reschedule_button"
        )

        self.cancel_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 510, 150, 40),
            text="Отменить",
            object_name="cancel_button"
        )

    def setup_labels(self):
        self.pair_edit = create_labeled_edit(
            parent=self,
            label_text="Номер пары:",
            value_text="",
            y=80,
            object_name="pair_edit"
        )

        self.subject_edit = create_labeled_edit(
            parent=self,
            label_text="Предмет:",
            value_text="",
            y=120,
            object_name="subject_edit"
        )

        self.subgroup_edit = create_labeled_edit(
            parent=self,
            label_text="Подгруппа:",
            value_text="",
            y=160,
            object_name="subgroup_edit"
        )

        self.room_edit = create_labeled_edit(
            parent=self,
            label_text="Аудитория:",
            value_text="",
            y=200,
            object_name="room_edit"
        )

        self.datetime_edit = create_labeled_edit(
            parent=self,
            label_text="Дата и время:",
            value_text="",
            y=240,
            object_name="datetime_edit"
        )

    def show_reschedule_dialog(self):
        groups = self.selected_groups
        new_pair = self.pair_edit.text()
        title = self.subject_edit.text()
        new_room = self.room_edit.text()
        new_date = self.datetime_edit.text()
        subgroup = self.subgroup_edit.text()

        if self.check_reschedule(groups, new_pair, title, new_room, subgroup, new_date):
            message = "Ошибка при создании переноса"
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("Информация о переносе")
            dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            dialog.setText(message)
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

            dialog.exec()
            return

        try:
            groups = self.dbManager.group_service.get_for_action(self.selected_groups, self.old_date,
                                                              title, subgroup, self.old_pair)

            if len(groups) > 1:
                groups_text = ", ".join(groups[:-1]) + ", " + groups[-1]
                message = (
                    f"Группы {groups_text}\n"
                    f"{title} с {self.old_date} переносится\n"
                    f"на {new_date} в аудиторию {new_room} на {new_pair} пару"
                )
            else:
                message = (
                    f"Группа {groups[0]}\n"
                    f"{title} с {self.old_date} переносится\n"
                    f"на {new_date} в аудиторию {new_room} на {new_pair} пару"
                )

            (self.dbManager.discipline_service.
             reschedule_discipline(self.selected_groups, self.old_date, self.old_pair,
                                   new_date, title, subgroup, new_pair, new_room, message))

            self.update_old_time(new_date)
            self.update_old_pair(new_pair)

        except RuntimeError as e:
            message = (
                f"Не удалось перенести пару.\n{e}"
            )
        except Exception as e:
            message = (
                f"Не удалось перенести пару. Данные введены некорректно"
            )

        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Информация о переносе")
        dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        dialog.setText(message)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

        dialog.addButton("Скопировать", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        dialog.exec()

        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(message)

    def check_reschedule(self, groups, pair, subject, room, subgroup, datetime_):
        return (not len(groups) or not len(pair) or not len(subject) or
                not len(room) or not len(datetime_)) or not len(subgroup)

    def show_cancel_dialog(self):
        groups = self.selected_groups
        pair = self.pair_edit.text()
        subject = self.subject_edit.text()
        room = self.room_edit.text()
        datetime_ = self.datetime_edit.text()
        subgroup = self.subgroup_edit.text()

        if self.check_reschedule(groups, pair, subject, room, subgroup, datetime_):
            message = "Не удалось удалить пару"
            dialog = QtWidgets.QMessageBox()
            dialog.setWindowTitle("Информация об отмене")
            dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            dialog.setText(message)
            dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

            dialog.exec()
            return

        try:
            groups = self.dbManager.group_service.get_for_action(self.selected_groups, self.old_date,
                                                                 subject, subgroup, self.old_pair)

            if len(groups) > 1:
                groups_text = ", ".join(groups[:-1]) + ", " + groups[-1]
                message = (
                    f"Группы {groups_text}\n"
                    f"{subject} {datetime_} на {pair} паре отменяется\n"
                )
            else:
                message = (
                    f"Группа {groups[0]}\n"
                    f"{subject} {datetime_} на {pair} паре отменяется\n"
                )

            self.dbManager.discipline_service.delete_discipline(groups, datetime_, subject, subgroup, pair, message)
        except:
            message = (
                f"Не удалось отменить пару. Данные введены некорректно\n"
            )

        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Информация об отмене")
        dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        dialog.setText(message)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

        dialog.addButton("Скопировать", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        dialog.exec()

        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(message)
        self.set_default_labels()

    def update_labels(self, info):
        self.pair_edit.setText(str(info[0]))
        self.subject_edit.setText(str(info[1]))
        self.room_edit.setText(str(info[2]))
        self.datetime_edit.setText(str(info[3]))
        self.subgroup_edit.setText(str(info[4]))
        self.update_old_time(info[3])
        self.update_old_pair(info[0])

    def set_default_labels(self):
        self.pair_edit.clear()
        self.subject_edit.clear()
        self.room_edit.clear()
        self.datetime_edit.clear()
        self.subgroup_edit.clear()

    def update_selected_groups(self, groups):
        self.selected_groups = groups

    def update_old_time(self, time: str):
        self.old_date = time

    def update_old_pair(self, pair: str):
        self.old_pair = pair

    def hide_panel(self):
        self.hide()

    def show(self):
        super().show()
