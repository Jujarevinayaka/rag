import os
from datetime import datetime

class HISTORY():
    def __init__(self):
        data_folder = os.getcwd() + "/history/"
        if not os.path.isdir(data_folder):
            os.makedirs(data_folder)

        file_prefix = datetime.now().strftime("%d%m%YT%H%M%S")
        self.__file_path = data_folder + file_prefix + "_db.csv"

    def _write(self, data):
        if os.path.isfile(self.__file_path):
            mode = 'a'
            header = False
        else:
            mode = 'w'
            header = True
        data.to_csv(self.__file_path, index=False, mode=mode, header=header)
