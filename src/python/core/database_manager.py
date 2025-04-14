import os

import psycopg2

from src.python.repositories.date_repository import DateRepository
from src.python.repositories.discipline_repository import DisciplineRepository
from src.python.repositories.group_repository import GroupRepository
from src.python.services.date_service import DateService
from src.python.services.discipline_service import DisciplineService
from src.python.services.group_service import GroupService
from Config import Config


class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST
        )

        self.group_service = GroupService(GroupRepository(self.connection))
        self.discipline_service = DisciplineService(DisciplineRepository(self.connection))
        self.date_service = DateService(DateRepository(self.connection))

    def close(self):
        self.connection.close()
