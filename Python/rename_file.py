import os


def rename_file():
	use_folder = "/home/seth/Udacity_FullStack/Python/prank"
	file_list = os.listdir(use_folder)

	# Lets get the current directory 
	saved_path = os.getcwd()
	print ("Current directory is: " + saved_path)
	os.chdir(use_folder)

	for file_name in file_list:
		os.rename(file_name, file_name.translate(None, "0123456789"))

	# Back to the  working directory
	os.chdir(saved_path)

rename_file()