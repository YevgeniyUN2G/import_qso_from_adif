# Функции для работы с БД
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import config
import sys
import settings

class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        try:
            self._connection = psycopg2.connect(
                     user = config.db_user,
                 password = config.db_password,
                     host = config.db_host,
                     port = config.db_port,
                 database = config.db_database)
            #print("Connection is succesful", self._connection)
            settings.logger.info("Connection is succesful %s", self._connection)
            self._cursor = self._connection.cursor()
            #print("_cursor ", self._cursor)
            settings.logger.info("_cursor %s", self._cursor)
            #return connection
        except (Exception, Error) as error:
            #print("Ошибка при работе с PostgreSQL", error)
            settings.logger.info("Ошибка при работе с PostgreSQL %s", error)
            sys.exit(5)


    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


    # def close_db(connection):
    #     if connection:
    #         connection.close()


    def get_name_files(self):
        print("self", self)
        sql = """
                 select tb.name_file, tb.id 
                   from public.import_adif tb 
                  where tb.result_import = 0
              """
        rows = self._cursor.execute(sql).fetchall()
        print(">>>", rows)
        settings.logger.info("Name of files", rows)
        return rows



# def connect_db():
#     try:
#         connection = psycopg2.connect(
#             user = "postgres",
#             password = "1234",
#             host = "127.0.0.1",
#             port = "5432",
#             database = "test2")
#         print("Connection is succesful")
#         return connection
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#
#
#
# def close_db(connection):
#     if connection:
#         connection.close()
