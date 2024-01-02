import os

def delete_directory(directory):
	if not os.path.exists(directory):
		return
	for root, dirs, files in os.walk(directory, topdown=False):
		for file in files:
			os.remove(os.path.join(root, file))

		# Add this block to remove folders
		for dir in dirs:
			os.rmdir(os.path.join(root, dir))
	return

def delete_file(file_name):
	if os.path.isfile(file_name):
		os.remove(file_name)

def create_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	return

def clear_directory(directory):
	delete_directory(directory)
	create_directory(directory)
	return

def create_file(file_name, contents):
	if not os.path.exists(file_name):
		with open(file_name, "w") as file:
			file.write(contents)
	return