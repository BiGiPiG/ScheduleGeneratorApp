from dataclasses import dataclass

from PyQt6.QtCore import QDate


@dataclass
class Discipline:
    pair: int
    title: str
    worktype: str


class DisciplineRepository:
    """Класс для работы с дисциплинами в базе данных"""

    def __init__(self, connection):
        """
        :param connection: активное подключение к БД
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def find_all_disciplines(self):
        query = """
            SELECT 
                DISTINCT r.pair, d.shorttitle, sc_worktypes.title
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
            JOIN sc_worktypes ON r.worktype = sc_worktypes.id 
            ORDER BY r.pair;
        """
        try:
            self.cursor.execute(query)
            return [Discipline(row[0], row[1], row[2])
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении предметов групп: {e}")
            return []

    def find_disciplines_by_groups(self, group_names):
        """Получить список дисциплин для списка групп"""
        query = """
            SELECT DISTINCT r.pair, d.shorttitle, sc_worktypes.title
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
            JOIN sc_worktypes ON r.worktype = sc_worktypes.id
            WHERE g.title = ANY(%s)
            ORDER BY r.pair;
        """

        try:
            self.cursor.execute(query, (group_names, ))
            return [Discipline(row[0], row[1], row[2])
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении предметов групп: {e}")
            return []

    def find_disciplines_by_groups_and_date(self, group_names, date):

        query = """
        SELECT DISTINCT r.pair, d.shorttitle, sc_worktypes.title
        FROM sc_group g
        JOIN sc_rasp18_groups rg ON g.id = rg.group_id
        JOIN sc_rasp18 r ON rg.rasp18_id = r.id
        JOIN sc_disc d ON r.disc_id = d.id
        JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
        JOIN sc_worktypes ON r.worktype = sc_worktypes.id
        WHERE g.title = ANY(%s) and sc_rasp18_days.day = %s
        ORDER BY r.pair;
        """

        try:
            self.cursor.execute(query, (group_names, date))
            return [Discipline(row[0], row[1], row[2])
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении предметов дисциплин: {e}")
            return []

    def find_all_discipline_information(self, group_names, date, title, work_type):
        query = """
                SELECT pair, d.shorttitle, sc_rasp18_rooms.room, sc_rasp18_days.day
                FROM sc_group g
                JOIN sc_rasp18_groups rg ON g.id = rg.group_id
                JOIN sc_rasp18 r ON rg.rasp18_id = r.id
                JOIN sc_disc d ON r.disc_id = d.id
                JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
                JOIN sc_worktypes ON r.worktype = sc_worktypes.id
                JOIN sc_rasp18_rooms ON r.id = sc_rasp18_rooms.rasp18_id
                WHERE g.title = ANY(%s) and sc_rasp18_days.day = %s and d.shorttitle = %s
                and sc_worktypes.title = %s
                """

        try:
            self.cursor.execute(query, (group_names, date, title, work_type))
            return [[row[0], row[1], row[2],
                    QDate(row[3].year, row[3].month, row[3].day).toString("yyyy-MM-dd")]
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении информации о предмете: {e}")
            return []

    def find_prep(self, group_names, date, title, work_type):
        query = """
            SELECT sc_prep.fio
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days rd ON r.day_id = rd.id
            JOIN sc_worktypes wt ON r.worktype = wt.id
            JOIN sc_rasp18_rooms rm ON r.id = rm.rasp18_id
            JOIN sc_rasp18_preps rp ON r.id = rp.rasp18_id
            JOIN sc_prep ON rp.prep_id = sc_prep.id
            WHERE g.title = ANY(%s)
              AND rd.day = %s
              AND d.shorttitle = %s
              AND wt.title = %s;
        """

        try:
            self.cursor.execute(query, (group_names, date, title, work_type))
            return [row[0]
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении информации о предмете: {e}")
            return []

