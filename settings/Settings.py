import os
import re


class Settings:

    def __init__(self, base_path):
        self.base_path = base_path

    def get_settings(self):

        path = os.path.join(self.base_path, 'settings.txt')
        dictionary_settings = {}

        with open(path, 'r') as archivo:
            lines = archivo.readlines()
            for line in lines:
                name_setting = re.search(r'.+=', line).group().replace('=', "")
                value_setting = re.search(r'=.+', line).group().replace('=', "")

                dictionary_settings[name_setting] = int(value_setting)

        return dictionary_settings

    def save_Settings(self, keys, values):

        path = os.path.join(self.base_path, 'settings.txt')

        with open(path, 'w') as file:

            for i in range(keys.__len__()):
                file.write(keys[i]+"="+str(values[i])+"\n")
