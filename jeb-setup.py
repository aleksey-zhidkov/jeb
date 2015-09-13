#!/usr/bin/python
import yaml

source = raw_input("Source dir: ")
if not source.endswith('/'):
    source += '/'

backupsDir = raw_input("Backups dir: ")
backupsCount = int(raw_input("Backups count: "))

hanoi = [[], [], []]
diskMappings = {}
for disk in range(backupsCount, 0, -1):
    hanoi[0].append(disk)
    diskMappings[disk] = None

jeb_state = {
    'source': source,
    'backups_dir': backupsDir,
    'hanoi': hanoi,
    'step': 0,
    'disks_mappings': diskMappings,
    'biggest_disk': backupsCount
}

f = open('/home/azhidkov/.config/jeb/data.yaml', "w")
yaml.dump(jeb_state, f)
f.close()
