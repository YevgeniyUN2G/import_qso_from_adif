# Из БД читаем название не обработанных файлов
# Берём файл в папке input
# Копируем файл в temp_work
# После обработки файла, копируем в temp_delete
import random
import parssing_adif_file
from library_bd import DBManager
import logging
import settings
from os import path
import shutil
import config


logger = logging.getLogger(__name__)


class HandlFiles:

    def __init__(self):
        self.BD = DBManager()

    # Выбираем названия файлов для импорта
    def read_name_files(self):
        sql = """
                SELECT name_file, id 
                FROM public.import_adif 
                WHERE result_import = 0;
              """
        self.BD._cursor.execute(sql)
        rows = self.BD._cursor.fetchall()
        for row in rows:
            settings.logger.info("Name of file %s", row)
            parssing_adif_file.ParssingADIF().open_file(row[0])
            id_handl_file = row[1]
            print(id_handl_file)
            settings.logger.info("Number of files in paket %s", id_handl_file)
            logger.info(id_handl_file)
            self.BD._connection.commit()
            HandlFiles.copy_file(config.path_input_adif_file, config.path_completed_file, row[0])
            HandlFiles.put_status_files(self, id_handl_file)
        settings.logger.info("Finished")

    def copy_file(dir_in, dir_out, name_file):
        full_name = dir_in + name_file
        if path.exists(full_name):
            if path.exists(dir_out + name_file):
                # переименовать файл
                tmp_nime_file = path.basename(full_name)
                next_id = (''.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(10)]))
                name_file = path.splitext(tmp_nime_file)[0] + '_' + next_id + path.splitext(tmp_nime_file)[1]
                #print("name_file ", name_file)
                new_location = shutil.move((full_name), (dir_out + name_file))
                settings.logger.info("% s перемещен в указанное место с новым именем, %s" % (name_file, new_location))
            else:
                new_location = shutil.move((full_name), dir_out)
                settings.logger.info("% s перемещен в указанное место, %s" % (name_file, new_location))
        else:
            #print("Файл не существует.")
            settings.logger.info("Файл %s не существует." % name_file)


    def put_status_files(self, id_handl_file):
        sql = "update public.import_adif set date_import = CURRENT_TIMESTAMP, result_import = 1 where id = " + str(id_handl_file) + ";"
        settings.logger.debug("sql change status file %s", sql)
        settings.logger.info("sql change status file %s", sql)
        settings.logger.info("File Id = %s status changed" % id_handl_file)
        result = self.BD._cursor.execute(sql)
        self.BD._connection.commit()