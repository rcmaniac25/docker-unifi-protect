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
ENV_SCRIPT = '/etc/default/unifi-protect'
ENV_SCRIPT_BAK = '/etc/default/unifi-protect.bak'

def startup_script():
	if not os.path.isfile(EXEC_SCRIPT):
		print("Creating startup script")

		sha = get_sha1(PRE_START)
		if sha != PRE_START_SHA1:
			print('pre-start has changed! This code may not work. Aborting')
			sys.exit(1)
		else:
			shutil.copy2(PRE_START, EXEC_SCRIPT)

			# Copying from one to another, removing all instances of tmpfs references and the "mount" line
			with open(EXEC_SCRIPT, "w") as dst:
				with open(PRE_START, "r") as src:
					for line in src:
						if not "mount" in line:
							dst.write(line)

			print('Startup script created')

def env_file():
	if not os.path.isfile(ENV_SCRIPT_BAK):
		print("Updating env file")

		shutil.copy2(ENV_SCRIPT, ENV_SCRIPT_BAK)

		with open(ENV_SCRIPT, "w") as dst:
			with open(ENV_SCRIPT_BAK, "r") as src:
				for line in src:
					if "UFP_TMPFS_DIR=" in line:
						dst.write("UFP_TMPFS_DIR=/tmp/unifi-protect\n")
					else:
						dst.write(line)

		print("Finished updating env file")

if __name__ == "__main__":
	startup_script()
	env_file()
