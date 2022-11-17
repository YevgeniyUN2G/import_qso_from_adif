import handling_files
import settings

if __name__ == '__main__':
    settings.logger.info("-------------------------------------------------------------------------------")
    settings.logger.info("Start")
    handling_files.HandlFiles().read_name_files()

