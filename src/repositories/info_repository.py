from dataclasses import dataclass


@dataclass
class Info:
    date: str
    action: str
    description: str


class InfoRepository:
    """Класс для работы с информацией о пеерносе в базе данных"""

    def __init__(self, connection):
        """
        :param connection: активное подключение к БД
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def find_all(self):
        query = """
            SELECT * FROM sc_rasp18_info;
        """

        try:
            self.cursor.execute(query)
            return [Info(row[3][0: 10], row[2], row[3][11:]) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении истории изменений: {e}")
            return []
