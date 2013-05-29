import os

user_home = os.path.expanduser('~')

# global config file
config_file_name = 'reminisc.ini'
config_folder_name = '.reminisc'
config_folder_path = os.path.join(user_home, config_folder_name)
config_file_path = os.path.join(config_folder_path, config_file_name)

# modules
module_config_file_name = 'config.ini'
modules_folder_name = 'modules'
modules_folder_path = os.path.join(config_folder_path, modules_folder_name)

# modules which are allowed to generate config files
approved_reminisc_modules = [
	'reminisc.modules.example_client_module',
	'reminisc.modules.gajim_import',
]

def get_global_config_path(main_dir_path):
	return os.path.join(main_dir_path, config_file_name)

def get_module_config_dir(main_dir_path, module_name):
	return os.path.join(main_dir_path, modules_folder_name, module_name)

def get_module_config_path(main_dir_path, module_name):
	return os.path.join(get_module_config_dir(main_dir_path, module_name), module_config_file_name)