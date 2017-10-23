#!/usr/bin/env python3
import plistlib
import subprocess
import sys
import time

TIMEOUT_SECONDS = 120
PARTITION_UUID = 'BB7841BE-7A13-4F6D-8E79-2E7AF1C3CCF4'

def main():
	ext_backup_disk = wait_for_and_find_ext_backup_disk()
	print('Found ext_backup Disk as '+ext_backup_disk)


def wait_for_and_find_ext_backup_disk():
	print('Wait for/find ext_backup Disk')
	progress = Progress()
	for i in range (0, TIMEOUT_SECONDS):
		backup_disk_identifier = find_ext_backup_disk()
		if backup_disk_identifier:
			progress.finish()
			return backup_disk_identifier

		progress.tick()
		time.sleep(1)

	raise RuntimeException('Could not find Ext-Backup Disk')

def find_ext_backup_disk():
	disks = list_disks()
	for disk in disks.get('AllDisksAndPartitions', []):
		for partition in disk.get('Partitions', []):
			if partition.get('DiskUUID') == PARTITION_UUID:
				return disk['DeviceIdentifier']

	return None

def list_disks():
	result = subprocess.run(['diskutil', 'list', '-plist'], stdout=subprocess.PIPE, check=True)
	parsed = plistlib.loads(result.stdout, fmt=plistlib.FMT_XML)
	return parsed

class Progress(object):
	def __init__(self):
		self.did_output = False

	def tick(self):
		self.did_output = True
		sys.stdout.write('.')
		sys.stdout.flush()

	def finish(self):
		if self.did_output:
			print('')

if __name__ == '__main__':
	main()
