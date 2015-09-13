#!/usr/bin/python

import sys
import os.path
import time
from subprocess import call
from os import listdir
from os.path import join

import yaml

logFile = '/var/log/jeb/jeb.log'

jeb_state_file = open('/home/azhidkov/.config/jeb/data.yaml')
jeb_state = yaml.safe_load(jeb_state_file)
jeb_state_file.close()

hanoi = jeb_state['hanoi']
step = jeb_state['step']
disk_mapping = jeb_state['disks_mappings']
source = jeb_state['source']
backup_dir = jeb_state['backups_dir']
biggest_disk = jeb_state['biggest_disk']

currentDate = sys.argv[1]
new_backup_name = backup_dir + '/' + currentDate


def peg_to_string(peg):
    return ' '.join(str(e) for e in peg)


def newest_backup(backup_dir):
    res = None
    newest_backup_time = None
    for f in listdir(backup_dir):
        f = join(backup_dir, f)
        ct = time.ctime(os.path.getctime(f))
        if res is None or newest_backup_time < ct:
            res = f
            newest_backup_time = ct

    return res


def move_disk(peg1, peg2):
    if len(hanoi[peg1]) == 0:
        from_peg = peg2
        to_peg = peg1
    elif len(hanoi[peg2]) == 0:
        from_peg = peg1
        to_peg = peg2
    elif hanoi[peg1][-1] > hanoi[peg2][-1]:
        from_peg = peg2
        to_peg = peg1
    else:
        from_peg = peg1
        to_peg = peg2

    disk = hanoi[from_peg].pop()
    hanoi[to_peg].append(disk)

    base_backup_name = newest_backup(backup_dir)
    old_backup_name = disk_mapping[disk]
    disk_mapping[disk] = new_backup_name

    if base_backup_name is None:
        print 'Create base backup'
        call(["cp", "-lr", source, new_backup_name])
    else:
        print 'Creating backup ' + new_backup_name + ' on base ' + base_backup_name
        call(["rsync", "-avh", "--delete", "--link-dest=" + base_backup_name, source, new_backup_name])
        # check that command finished successfully

    if old_backup_name is not None:
        if disk_mapping[biggest_disk] is None:
            print 'Storing backup' + old_backup_name + ' to the biggest/latest (' + str(biggest_disk) + ') peg/tape'
            disk_mapping[biggest_disk] = old_backup_name
        else:
            print 'Removing backup ' + old_backup_name
            call(["rm", "-rf", old_backup_name])


def done():
    return len(hanoi[0]) == 0 and len(hanoi[1]) == 0


def print_hanoi():
    print peg_to_string(hanoi[0])
    print peg_to_string(hanoi[1])
    print peg_to_string(hanoi[2])
    print '======'


if os.path.isdir(new_backup_name):
    print 'Backup ' + new_backup_name + ' already exist'
    sys.exit(0)

if done():
    print 'reset'
    hanoi[0] = hanoi[2]
    print_hanoi()
    hanoi[2] = []
    print_hanoi()

if step % 3 == 0:
    move_disk(0, 1)
elif step % 3 == 1:
    move_disk(0, 2)
else:
    move_disk(1, 2)

print_hanoi()
jeb_state['step'] += 1

jeb_state_file = open('/home/azhidkov/.config/jeb/data.yaml', "w")
yaml.dump(jeb_state, jeb_state_file)
jeb_state_file.close()
