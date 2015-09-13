#!/bin/sh

echo "Backingup Yandex.Disk"
date
echo "Sync Yandex.Disk"
yandex-disk sync -c ~/.config/yandex-disk/config-backup.cfg --read-only --overwrite
currentDate=$(date +"%y%m%d")
echo "Create backup for $currentDate"
/usr/lib/jeb/jeb-backup.py $currentDate
echo "====================="
