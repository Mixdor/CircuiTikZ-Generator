import re


class Settings:

    def get_settings(self):

        dictionary_settings = {}

        with open('settings.txt', 'r') as archivo:
            lines = archivo.readlines()
            for line in lines:
                name_setting = re.search(r'.+=', line).group().replace('=', "")
                value_setting = re.search(r'=.+', line).group().replace('=', "")

                dictionary_settings[name_setting] = int(value_setting)

        return dictionary_settings

    def save_Settings(self, keys, values):

        with open('settings.txt', 'w') as file:

            for i in range(keys.__len__()):
                file.write(keys[i]+"="+str(values[i])+"\n")
