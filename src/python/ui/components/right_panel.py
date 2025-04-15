from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHBoxLayout


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
        self.selected_groups = ["КМБО-23-24"]
        self.setup_ui()

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
            geometry=QtCore.QRect(x_position, 410, 150, 40),
            text="Перенести",
            object_name="reschedule_button"
        )
        self.reschedule_button.clicked.connect(self.show_reschedule_dialog)

        self.cancel_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 480, 150, 40),
            text="Отменить",
            object_name="cancel_button"
        )

        self.cancel_button.clicked.connect(self.show_cancel_dialog)
        self.add_button = create_button(
            parent=self,
            geometry=QtCore.QRect(x_position, 550, 150, 40),
            text="Добавить",
            object_name="add_button"
        )

    def setup_labels(self):
        self.pair_edit = create_labeled_edit(
            parent=self,
            label_text="Номер пары:",
            value_text="6",
            y=80,
            object_name="pair_edit"
        )

        self.subject_edit = create_labeled_edit(
            parent=self,
            label_text="Предмет:",
            value_text="Введение в разработку ПО",
            y=120,
            object_name="subject_edit"
        )

        self.teacher_edit = create_labeled_edit(
            parent=self,
            label_text="Преподаватель:",
            value_text="Иванов И.И.",
            y=160,
            object_name="teacher_edit"
        )

        self.room_edit = create_labeled_edit(
            parent=self,
            label_text="Аудитория:",
            value_text="ИВЦ-101",
            y=200,
            object_name="room_edit"
        )

        self.datetime_edit = create_labeled_edit(
            parent=self,
            label_text="Дата и время:",
            value_text="08.04.2025",
            y=240,
            object_name="datetime_edit"
        )

    def show_reschedule_dialog(self):
        groups = self.selected_groups
        pair = self.pair_edit.text()
        subject = self.subject_edit.text()
        teacher = self.teacher_edit.text()
        room = self.room_edit.text()
        datetime_ = self.datetime_edit.text()

        try:
            new_date = datetime_.split()[0]
            old_date = "07.04.2025"
        except Exception:
            new_date = datetime_
            old_date = "..."

        if len(groups) > 1:
            groups_text = ", ".join(groups[:-1]) + ", " + groups[-1]
            message = (
                f"Группы {groups_text}\n"
                f"{subject} с {old_date} переносится\n"
                f"на {new_date} в аудиторию {room} на {pair} пару"
            )
        else:
            message = (
                f"Группа {groups[0]}\n"
                f"{subject} с {old_date} переносится\n"
                f"на {new_date} в аудиторию {room} на {pair} пару"
            )

        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Информация о переносе")
        dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        dialog.setText(message)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

        copy_button = dialog.addButton("Скопировать", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        dialog.exec()

        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(message)

    def show_cancel_dialog(self):
        groups = self.selected_groups
        pair = self.pair_edit.text()
        subject = self.subject_edit.text()
        teacher = self.teacher_edit.text()
        room = self.room_edit.text()
        datetime_ = self.datetime_edit.text()

        message = (
            f"Группа {groups[0]}\n"
            f"{subject} {datetime_} на {pair} паре отменяется\n"
        )

        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Информация об отмене")
        dialog.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        dialog.setText(message)
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)

        copy_button = dialog.addButton("Скопировать", QtWidgets.QMessageBox.ButtonRole.ActionRole)

        dialog.exec()

        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(message)

    def update_labels(self, info, prep):
        self.pair_edit.setText(str(info[0][0]))
        self.subject_edit.setText(str(info[0][1]))
        self.teacher_edit.setText(prep)
        self.room_edit.setText(str(info[0][2]))
        self.datetime_edit.setText(str(info[0][3]))

    def update_selected_groups(self, groups):
        self.selected_groups = groups


