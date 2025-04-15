from typing import List
from datetime import date

from src.python.repositories.discipline_repository import Discipline


class DisciplineService:
    """Сервис для работы с учебными дисциплинами"""

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

    def get_by_groups_and_date(self, group_names: List[str], date: date) -> List[Discipline]:
        """Получить расписание по группам и дате"""
        return self.db.find_disciplines_by_groups_and_date(group_names, date)

    def get_all_discipline_information(self, group_names, date, title, work_type):
        return self.db.find_all_discipline_information(group_names, date, title, work_type)

    def get_prep(self, group_names, date, title, work_type):
        return self.db.find_prep(group_names, date, title, work_type)

