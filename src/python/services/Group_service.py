from typing import List
from dataclasses import dataclass


@dataclass
class Group:
    id: int
    name: str


class GroupService:
    """Сервис для работы с учебными группами"""

    def __init__(self, db_repository):
        """
        :param db_repository: Репозиторий для работы с БД
        """
        self.db = db_repository

    def get_all(self) -> List[Group]:
        """Получить все группы"""
        return self.db.find_all_groups()

    def get_by_discipline(self, discipline_name: str) -> List[Group]:
        """Получить группы по дисциплине"""
        return self.db.find_groups_by_discipline(discipline_name)
