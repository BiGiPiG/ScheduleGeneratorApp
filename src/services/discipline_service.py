from dataclasses import dataclass
from typing import List
from datetime import date

from src.repositories.discipline_repository import Discipline


@dataclass
class TimeSlot:
    """Класс для хранения временного интервала пары"""
    start: str
    end: str


class DisciplineService:
    """Сервис для работы с учебными дисциплинами"""

    PAIR_TIMES = {
        1: TimeSlot("9:00", "10:30"),
        2: TimeSlot("10:40", "12:10"),
        3: TimeSlot("12:40", "14:10"),
        4: TimeSlot("14:20", "15:50"),
        5: TimeSlot("16:20", "17:50"),
        6: TimeSlot("18:00", "19:30")
    }

    def __init__(self, db_repository):
        """
        :param db_repository: Репозиторий для работы с БД
        """
        self.db = db_repository

    def get_all(self) -> List[Discipline]:
        """Получить все дисциплины"""
        return self.db.find_all_disciplines()

    def get_by_groups(self, group_names: List[str]) -> List[Discipline]:
        """Получить дисциплины по списку групп"""
        return self.db.find_disciplines_by_groups(group_names)

    def get_by_groups_and_date(self, group_names: List[str], query_date: date) -> List[Discipline]:
        """Получить расписание по группам и дате"""
        return self.db.find_disciplines_by_groups_and_date(group_names, query_date)

    def get_all_discipline_information(self, group_names, query_date, title, work_type):
        return self.db.find_all_discipline_information(group_names, query_date, title, work_type)

    def delete_discipline(self, group_names, datetime_, title, subgroup, pair, message):
        info = self.db.find_id(group_names, datetime_, title, subgroup, pair)
        if len(info):
            self.db.delete_discipline(info[0], message)
        else:
            print("YНе удалось найти пару")
            raise RuntimeError("Не удалось найти пару")

    def reschedule_discipline(self, group_names, old_date, old_pair,
                              new_date, title, subgroup, new_pair, room, message):

        if len(self.db.check_time_for_reschedule(group_names, new_date, new_pair)):
            raise RuntimeError("Данное время уже занято")
        if len(self.db.check_room_for_reschedule(room, new_date, new_pair)):
            raise RuntimeError("Данная аудитория уже занята")

        self.db.db_reschedule_discipline(
            *self.db.find_id(group_names, old_date, title, subgroup, old_pair),
            new_pair,
            new_date,
            self.PAIR_TIMES[int(new_pair)],
            message
        )
