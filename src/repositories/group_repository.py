from dataclasses import dataclass


@dataclass
class Group:
    id: int
    name: str


class GroupRepository:
    """Класс для работы с группами в базе данных"""

    def __init__(self, connection):
        """
        :param connection: активное подключение к БД
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def find_all_groups(self):
        try:
            self.cursor.execute("SELECT title FROM sc_group ORDER BY title")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка при получении групп: {e}")
            return []

    def find_by_groups(self, group_names):
        query = """
            SELECT title FROM 
                sc_group 
            WHERE 
                SUBSTRING(title, 9, 2) LIKE %s
                and SUBSTRING(title, 1, 4) LIKE %s;
        """
        try:
            self.cursor.execute(query, (group_names[0][8:], group_names[0][0:4]))
            return [row[0] for row in self.cursor.fetchall()]

        except Exception as e:
            error_msg = f"Ошибка при получении групп по предмету '{group_names}': {str(e)}"
            print(error_msg)
            return []

    def find_groups_by_discipline(self, discipline_name):
        query = """
            SELECT DISTINCT sc_group.title FROM sc_rasp18_groups 
            JOIN sc_rasp18 ON rasp18_id = sc_rasp18.id  
            JOIN sc_disc ON sc_rasp18.disc_id = sc_disc.id 
            JOIN sc_group ON group_id = sc_group.id 
            JOIN sc_worktypes ON sc_rasp18.worktype = sc_worktypes.id
            WHERE sc_disc.shorttitle = %s;
        """

        try:
            self.cursor.execute(query, (discipline_name, ))
            return [row[0] for row in self.cursor.fetchall()]

        except Exception as e:
            error_msg = f"Ошибка при получении групп по предмету '{discipline_name}': {str(e)}"
            print(error_msg)
            return []

    def find_for_action(self, rasp_id):
        query = """
            SELECT DISTINCT sc_group.title 
            FROM sc_rasp18_groups 
            JOIN sc_group ON group_id = sc_group.id 
            WHERE sc_rasp18_groups.rasp18_id = %s;
        """

        try:
            self.cursor.execute(query, (rasp_id, ))
            return [row[0] for row in self.cursor.fetchall()]

        except Exception as e:
            error_msg = f"Ошибка при получении групп для действия {str(e)}"
            print(error_msg)
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