import os
import shutil
import logging

import reminisc.config.defaults as defaults
import reminisc.config.reader as configreader
import reminisc.modules.utils as utils

logger = logging.getLogger(__name__)

def create_config_directory(path):
	# create directories
	if not os.path.isdir(path):
		os.mkdir(path)

	# save global config file
	global_config_path = defaults.get_global_config_path(path)
	if not os.path.isfile(global_config_path):
		shutil.copyfile('reminisc/config/default_config.ini', global_config_path)

	# save config files for all modules
	for reminisc_module_name in defaults.approved_reminisc_modules:
		reminisc_module_impls = utils.find_reminisc_module_implementations(reminisc_module_name)

		if len(reminisc_module_impls) > 1:
			logger.error("Reminisc module {} defines more than one module class. Config will not be generated"
				.format(reminisc_module_name))
		else:
			for impl in reminisc_module_impls:
				module_dir = defaults.get_module_config_dir(path, reminisc_module_name)
				module_config = defaults.get_module_config_path(path, reminisc_module_name)

				if not os.path.isdir(module_dir):
					os.makedirs(module_dir)

				if not os.path.isfile(module_config):
					config_file = open(module_config, 'w')
					config_file.write(impl.default_config())
					config_file.close()
