from dataclasses import dataclass


@dataclass
class Date:
    date: str


class DateRepository:
    """Класс для работы с датами в базе данных"""

    def __init__(self, connection):
        """
        :param connection: активное подключение к БД
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def find_by_discs_and_groups(self, disc, w_type, group_names):
        query = """
            SELECT DISTINCT sc_rasp18_days.day
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
            JOIN sc_worktypes ON r.worktype = sc_worktypes.id
            WHERE g.title = ANY(%s) and d.shorttitle = %s and sc_worktypes.title = %s
            ORDER BY sc_rasp18_days.day;
        """

        try:
            self.cursor.execute(query, (group_names, disc, w_type))
            return [row[0].strftime("%Y-%m-%d") for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении дат: {e}")
            return []
