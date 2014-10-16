import os
import sys

import hashlib
import shutil

import traceback

# Bit by Bit file copy utility

def checksum(path, hasher, blocksize = 2**16):

	if (os.path.isfile(path) == False):
		raise Exception("Checksum failed! Path not a file " + path)

	with open(path, 'rb') as handle:

		while (True):

			block = handle.read(blocksize)

			if (len(block) == 0):
				break

			hasher.update(block)
			
		handle.close()

		return hasher.digest()

	raise Exception("Checksum failed to open file " + path)

def transfer(source_path, destination_path):

	# Resolve paths
	source_path = os.path.realpath(source_path)
	destination_path = os.path.realpath(destination_path)

	# Verify that source path exists
	if (os.path.exists(source_path) == False):
		raise Exception("Source path does not exist " + source_path)

	# Verify that source path is a file
	if (os.path.isfile(source_path) == False):
		raise Exception("Source path is not a file " + source_path)

	# Verify that destination path exists
	if (os.path.exists(destination_path) == False):
		raise Exception("Destination path does not exist " + destination_path)

	# Verify that destination path is a directory
	if (os.path.isdir(destination_path) == False):
		raise Exception("Destination path is not a directory " + destination_path)

	# Perform checksum on source file
	source_digest = checksum(source_path, hashlib.sha256())

	# Build distination file path
	destination_path = os.path.join(destination_path, os.path.basename(source_path))

	# Check if file has already transfered...
	if (os.path.isfile(destination_path) == True):
		if (source_digest == checksum(destination_path, hashlib.sha256())):
			print("Success, file already transfered!")
			return
		else:
			print("Attempting to correct corrupted file...")

	# Copy over file and stats
	shutil.copyfile(source_path, destination_file_path)
	shutil.copystat(source_path, destination_file_path)

	# Verify transfer...
	if (source_digest == checksum(destination_file_path, hashlib.sha256())):
		print("Success, file transfered!")
		return

	raise Exception("File transfer failed because checksum failed!")

##### ##### ##### ##### ##### 
##### RUN PROGRAM
##### ##### ##### ##### ##### 

source_path		= sys.argv[1] # Source file
destination_path	= sys.argv[2] # Destination directory

try:
	transfer(source_path, destination_path)

except:
	print(traceback.format_exc())
