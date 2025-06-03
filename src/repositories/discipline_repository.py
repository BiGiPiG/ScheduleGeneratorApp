import traceback
from dataclasses import dataclass
from datetime import date

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
            SELECT DISTINCT d.shorttitle, sc_worktypes.title
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
            JOIN sc_worktypes ON r.worktype = sc_worktypes.id
            WHERE d.id IN (
                SELECT d2.id
                FROM sc_group g2
                JOIN sc_rasp18_groups rg2 ON g2.id = rg2.group_id
                JOIN sc_rasp18 r2 ON rg2.rasp18_id = r2.id
                JOIN sc_disc d2 ON r2.disc_id = d2.id
                WHERE g2.title = ANY(%s)
                GROUP BY d2.id
                HAVING COUNT(DISTINCT g2.title) = (SELECT COUNT(*) FROM sc_group WHERE title = ANY(%s))
            )
            GROUP BY d.shorttitle, sc_worktypes.title;
        """

        try:
            self.cursor.execute(query, (group_names, group_names))
            return [Discipline(-1, row[0], row[1])
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
        query_main = """
             SELECT pair, \
                    d.shorttitle, \
                    sc_rasp18_days.day, \
                    rg.subgroup, \
                    rg.rasp18_id
             FROM sc_group g
                      JOIN sc_rasp18_groups rg ON g.id = rg.group_id
                      JOIN sc_rasp18 r ON rg.rasp18_id = r.id
                      JOIN sc_disc d ON r.disc_id = d.id
                      JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
                      JOIN sc_worktypes ON r.worktype = sc_worktypes.id
             WHERE g.title = ANY (%s)
               AND sc_rasp18_days.day = %s
               AND d.shorttitle = %s
               AND sc_worktypes.title = %s \
         """

        query_room = """
         SELECT room \
         FROM sc_rasp18_rooms \
         WHERE rasp18_id = %s \
         """

        try:
            self.cursor.execute(query_main, (group_names, date, title, work_type))
            rows = self.cursor.fetchall()
            results = []
            for pair, shorttitle, day, subgroup, rasp18_id in rows:
                self.cursor.execute(query_room, (rasp18_id,))
                room_row = self.cursor.fetchone()
                room = room_row[0] if room_row is not None else "Не найдено"
                date_str = QDate(day.year, day.month, day.day).toString("yyyy-MM-dd")
                results.append([pair, shorttitle, room, date_str, subgroup])
            return results
        except Exception as e:
            print(f"Ошибка при получении информации о предмете: {e}")
            return []

    def find_id(self, group_names, date, title, subgroup, pair):
        query = """
            SELECT DISTINCT r.id
            FROM sc_group g
            JOIN sc_rasp18_groups rg ON g.id = rg.group_id
            JOIN sc_rasp18 r ON rg.rasp18_id = r.id
            JOIN sc_disc d ON r.disc_id = d.id
            JOIN sc_rasp18_days ON sc_rasp18_days.id = r.day_id
            WHERE g.title = ANY(%s) and sc_rasp18_days.day = %s and d.shorttitle = %s
            and rg.subgroup = %s
            and r.pair = %s
        """

        try:
            self.cursor.execute(query, (group_names, date, title, subgroup, pair))
            return [row[0]
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении id дня: {e}")
            return []

    def check_time_for_reschedule(self, groups, check_date, pair):
        groups = tuple(groups)
        query = """
                SELECT DISTINCT
                    r.id
                FROM 
                    sc_rasp18 r
                JOIN 
                    sc_rasp18_days d ON r.day_id = d.id
                JOIN 
                    sc_rasp18_groups g ON r.id = g.rasp18_id
                JOIN 
                    sc_group gr ON g.group_id = gr.id
                WHERE 
                    gr.title IN %s
                    AND d.day = %s
                    AND r.pair = %s;
                """
        print(groups, check_date, pair)
        try:
            self.cursor.execute(query, (groups, check_date, pair))
            return [row[0]
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при проверке времени: {e}")
            raise Exception("Не удалось проверить доступность времени для переноса")

    def check_room_for_reschedule(self, room, date, pair):
        query = """
                SELECT DISTINCT
                    rm.room
                FROM 
                    sc_rasp18 r
                JOIN 
                    sc_rasp18_days d ON r.day_id = d.id
                JOIN 
                    sc_rasp18_groups g ON r.id = g.rasp18_id
                JOIN 
                    sc_group gr ON g.group_id = gr.id
                LEFT JOIN 
                    sc_rasp18_rooms rm ON r.id = rm.rasp18_id
                WHERE 
                    rm.room = %s
                    AND d.day = %s
                    AND r.pair = %s;
                """
        print(room, date, pair)
        try:
            self.cursor.execute(query, (room, date, pair))
            return [row[0]
                    for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при проверке аудитории: {e}")
            raise Exception("Не удалось проверить доступность аудитории для переноса")

    def delete_discipline(self, rasp18_id, message):
        cur_date = date.today().strftime("%Y-%m-%d")
        message = f"{cur_date} {message}"
        try:

            self.cursor.execute("START TRANSACTION")

            insert_log_query = """
                INSERT INTO sc_rasp18_info (rasp18_id, kind, info)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(insert_log_query, (rasp18_id, 1, message))
            print(message)

            delete_queries = [
                "DELETE FROM sc_rasp18_groups WHERE rasp18_id = %s",
                "DELETE FROM sc_rasp18_preps WHERE rasp18_id = %s",
                "DELETE FROM sc_rasp18_rooms WHERE rasp18_id = %s",
                "DELETE FROM sc_rasp18 WHERE id = %s",
            ]

            for query in delete_queries:
                self.cursor.execute(query, (rasp18_id,))

            self.cursor.execute("COMMIT")
            print("Пара успешно удалена")

        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f"Ошибка при удалении пары: {e}")

    def db_reschedule_discipline(self, rasp_id, new_pair, new_day, new_times, message):
        try:
            cur_date = date.today().strftime("%Y-%m-%d")
            message = f"{cur_date} {message}"
            self.cursor.execute("START TRANSACTION")

            insert_log_query = """
                INSERT INTO sc_rasp18_info (rasp18_id, kind, info)
                VALUES (%s, %s, %s)
            """

            self.cursor.execute(insert_log_query, (rasp_id, 2, message))

            reschedule_query = """
                UPDATE sc_rasp18
                SET 
                    pair = %s,
                    timestart = %s,
                    timeend = %s,
                    day_id = (SELECT id FROM sc_rasp18_days WHERE day = %s)
                WHERE id = %s;
            """

            self.cursor.execute(reschedule_query, (new_pair, new_times.start, new_times.end, new_day, rasp_id))

            self.cursor.execute("COMMIT")
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            traceback.print_exc()
            # print(f"Ошибка при переносе пары: {e}")
            raise Exception("Ошибка при работе с бд")

    def check_discipline(self, title):
        query = """
        SELECT id FROM sc_disc WHERE shorttitle LIKE %s;
        """

        try:
            self.cursor.execute(title)
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при отмене: {e}")
            raise Exception("Была введена некорректная дисциплина")

    def check_room(self, room):
        query = """
        SELECT id FROM sc_rasp18_rooms WHERE room LIKE %s;
        """

        try:
            self.cursor.execute(room)
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при отмене: {e}")
            raise Exception("Была введена некорректная аудитория")

