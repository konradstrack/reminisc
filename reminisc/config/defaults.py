import os

user_home = os.path.expanduser('~')

config_file_name = 'reminisc.ini'
config_folder_name = '.reminisc'
config_folder_path = os.path.join(user_home, config_folder_name)
config_file_path = os.path.join(config_folder_path, config_file_name)