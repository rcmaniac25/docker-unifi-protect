#!/usr/bin/python3
# fake's being the ubnt-tool as UniFi Protect 1.13.3 doesn't want people to run software installs

# Interesting note: the regex UP uses does the following:
# 1. get the UUID
# 2. remove the '-'s
# 3. check against a UUID regex (that doesn't take '-' into account) AND get a specific charecter (xxxxxxxx-xxxx-5xxx-Nxxx-xxxxxxxxxxxx. Note, the N is [89ab])
# 4. if the specific charecter is the number 5, it's "registered" (which I think means it's registered with Ubiquiti), else you get a critical log stating it's not registered

import sys
import os
import uuid
import random

TOOL_ID_FILE_SRC = '/tool_id_src'
TOOL_ID_FILE_DST = '/srv/unifi-protect/data/tool_id'

def id_get_uuid():
	# excessive AND semi-useless, but we want a UUID that will be consistant through container runs AND has enough uniqueness
	random.seed(uuid.getnode())

	unique_id = uuid.UUID("{0:08x}-{1:04x}-5{2:03x}-{3}{4:03x}-{5:012x}".format(random.randint(0, 0xffffffff), random.randint(0, 0xffff), random.randint(0, 0xfff), random.choice(['8', '9', 'a', 'b']), random.randint(0, 0xfff), uuid.getnode()))
	return str(unique_id)

def id_cmd():
	if not os.path.isfile(TOOL_ID_FILE_DST):
		with open(TOOL_ID_FILE_DST, "w") as dst:
			with open(TOOL_ID_FILE_SRC, "r") as src:
				for line in src:
					if "board.uuid=" in line:
						dst.write("board.uuid={0}\n".format(id_get_uuid()))
					else:
						dst.write(line)

	#XXX may want to check that the UUID matches (if system changes, we want a different UUID)

	with open(TOOL_ID_FILE_DST, "r") as file:
		data = file.read()
		print(data)

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == "id":
		id_cmd()
	else:
		print("Unknown arguments: {0}".format(sys.argv))
		sys.exit(1)
