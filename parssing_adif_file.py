# input a name file by adif


from os import path
import config
import re
import config_tags_adif
import parssing_qsos
import settings
from library_bd import DBManager


class ParssingADIF:

    def __init__(self):
        self.BD = DBManager()


    # get charset encoding of file
    def get_encoding(self, file):
        with open((file), "r") as f:
            encoding_file = f.encoding
            f.close()
            return encoding_file


    def get_info_once_qso(self, line):
        qso_tags_info = {}
        for tag in config_tags_adif.tags:
            match = re.search(f"<{tag}:([0-9]+)>[\d\w,-]+", line)
            if match == None:
                continue
            tag_plus_info = line[match.span()[0]:match.span()[1]]
            start_cut_position = tag_plus_info.find('>')
            result = tag_plus_info[start_cut_position+1:]
            qso_tags_info[tag] = result
        return qso_tags_info


    def pars_line_to_qso(self, log_all):
        for line in log_all:
            result = self.get_info_once_qso(line)
            parssing_qsos.CreateSQL().create_sql_qso(result)


    def read_file_adif(self, text):
        all_log =[]
        index = 0
        str_with_eoh = 0
        len_text = len(text)
        # Find line of start QSOs
        for line in text:
            index += 1
            if line.find('<EOH>') == 0:
                str_with_eoh = index
        i = str_with_eoh
        qso_collect = ''
        while True:
            if len(text[i]) > 0:
                if (text[i].strip().find('<EOR>') != -1) and (text[i].strip().find('<EOR>') != 0):
                    qso = text[i].strip()
                    all_log.append(qso)
                elif (text[i].strip().find('<') != -1) and (text[i].strip().find('<EOR>') == -1):
                    qso_collect = qso_collect + text[i].strip()
                elif text[i].strip().find('<EOR>') != 0:
                    qso_collect = qso_collect + text[i].strip()
                elif text[i].strip().find('<EOR>') == 0:
                    qso_collect = qso_collect + text[i].strip()
                    all_log.append(qso_collect)
                    qso_collect = ''
            i += 1
            if i == len_text:
                break
        return all_log


    def open_file(self, name_file):
        name_file = config.path_input_adif_file + name_file
        # Check file exists
        if path.exists(name_file):
            coding_page = self.get_encoding(name_file)
            with open((name_file), "r", encoding=coding_page) as file_read:
                text = file_read.readlines()
                log = self.read_file_adif(text)
                self.pars_line_to_qso(log)
        else:
            settings.logger.info("Файл %s не существует." % name_file)