import psycopg2

from src.python.repositories.Date_repository import DateRepository
from src.python.repositories.Discipline_repository import DisciplineRepository
from src.python.repositories.Group_repository import GroupRepository
from src.python.services.Date_service import DateService
from src.python.services.Discipline_service import DisciplineService
from src.python.services.Group_service import GroupService


class DatabaseManager:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="schedule_db",
            user="postgres",
            password="uhuvid45",
            host="localhost"
        )

        self.group_service = GroupService(GroupRepository(self.connection))
        self.discipline_service = DisciplineService(DisciplineRepository(self.connection))
        self.date_service = DateService(DateRepository(self.connection))

    def close(self):
        self.connection.close()
