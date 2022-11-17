# На входе строка из adif фала
# На выходе - словарь с данными
import config_tags_adif
from library_bd import DBManager
import settings

class CreateSQL:

    def __init__(self):
        self.BD = DBManager()

    def create_sql_qso(self, data_qso):
        #print(data_qso)
        settings.logger.debug("data_qso %s", data_qso)
        insert_part = "INSERT INTO qsos2 ("
        values_part =') VALUES ('
        len_dict_qso = len(data_qso)
        index_qso_data = 0
        for index, key_dict_qso in enumerate(data_qso):
            index_qso_data += 1
            if key_dict_qso in config_tags_adif.tags:
                # tags CALL, NAME, STATE, MODE, OPERATOR are reserved key words in PostgreSQL
                key_dict_qso_repl = key_dict_qso
                if key_dict_qso == 'CALL':
                    key_dict_qso_repl = 'callsign'
                elif key_dict_qso == 'NAME':
                    key_dict_qso_repl = 'operator_name'
                elif key_dict_qso == 'STATE':
                    key_dict_qso_repl = 'name_state'
                elif key_dict_qso == 'MODE':
                    key_dict_qso_repl = 'qso_mode'
                elif key_dict_qso == 'OPERATOR':
                    key_dict_qso_repl = 'station_operator'

                if index_qso_data == len_dict_qso:
                    insert_part = insert_part + " " + key_dict_qso_repl + " "
                else:
                    insert_part = insert_part + " " + key_dict_qso_repl + ", "
                if index_qso_data == len_dict_qso:
                    values_part = values_part + " '" + data_qso[key_dict_qso] + "' "
                else:
                    values_part = values_part + " '" + data_qso[key_dict_qso] + "', "
        values_part = values_part + ');'
        sql = insert_part + values_part
        #print(sql)
        settings.logger.debug("sql %s", sql)
        #connection = DBManager()
        #print("connection ", connection )
        #cursor = connection.cursor()
        result = self.BD._cursor.execute(sql)
        #print(result)
        #settings.logger.debug("Response DB %s", result)
        return insert_part + values_part