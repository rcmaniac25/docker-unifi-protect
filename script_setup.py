#!/bin/python3
# The easy solution is to just copy the contents of the script into the Dockerfile init script...
# But that's technically copyright content that is not necessarily legal for me to publish online...
# Solution: runtime copy and modify of the file so there's no copyright content here

import sys
import os
import shutil
import hashlib

def get_sha1(file):
	with open(file, 'r') as f:
		data = f.read()

		h = hashlib.sha1(data.encode("UTF-8"))
		return h.hexdigest()

PRE_START = '/usr/share/unifi-protect/app/hooks/pre-start'
PRE_START_SHA1 = 'b7cb38f197dc4b102393f7c870cede50751291e6' # ----------------------- sha calculated when writing this script
EXEC_SCRIPT = '/usr/share/unifi-protect/app/hooks/docker_pre_start'
EXEC_SCRIPT_TMP = '/usr/share/unifi-protect/app/hooks/docker_pre_start.modding'

if __name__ == "__main__":
	if not os.path.isfile(EXEC_SCRIPT):
		print("Creating startup script")

		sha = get_sha1(PRE_START)
		if sha != PRE_START_SHA1:
			print('pre-start has changed! This code may not work. Aborting')
			sys.exit(1)
		else:
			# first copy is to read from, the 2nd is to get permissions and whatnot easily and then change the contents
			shutil.copy2(PRE_START, EXEC_SCRIPT_TMP)
			shutil.copy2(PRE_START, EXEC_SCRIPT)

			# Copying from one to another, removing all instances of tmpfs references and the "mount" line
			with open(EXEC_SCRIPT, "w") as dst:
				with open(EXEC_SCRIPT_TMP, "r") as src:
					for line in src:
						if '"$UFP_TMPFS_DIR"' in line:
							if not "mount" in line:
								dst.write(line.replace('"$UFP_TMPFS_DIR" ', ''))
						else:
							dst.write(line)

			os.remove(EXEC_SCRIPT_TMP)

			print('Startup script created')
			