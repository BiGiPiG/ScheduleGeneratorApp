class InfoService:

    def __init__(self, db_repository):
        """
        :param db_repository: Репозиторий для работы с БД
        """
        self.db = db_repository

    def get_all(self):
        return self.db.find_all()
