class DateService:
    """Сервис для работы с учебными дисциплинами"""

    def __init__(self, db_repository):
        """
        :param db_repository: Репозиторий для работы с БД
        """
        self.db = db_repository

    def get_by_discs_and_groups(self, disc, w_type, group_names):
        return self.db.find_by_discs_and_groups(disc, w_type, group_names)
    