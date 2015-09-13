#!/bin/sh

mkdir -p ~/.config/jeb
sudo mkdir -p /var/log/jeb
sudo chmod a+w /var/log/jeb
sudo mkdir -p /usr/lib/jeb
sudo cp -f backup-yandex-disk.sh /usr/lib/jeb
sudo cp -f jeb-backup.py /usr/lib/jeb
sudo cp -f jeb-setup.py /usr/lib/jeb
sudo chmod +x /usr/lib/jeb/*

rm -f /tmp/jeb.cron
crontab -l > /tmp/jeb.cron
sed -i '/\/usr\/lib\/jeb/d' /tmp/jeb.cron
echo "@reboot /usr/lib/jeb/backup-yandex-disk.sh >> /var/log/jeb/jeb.log" >> /tmp/jeb.cron
echo "@daily /usr/lib/jeb/backup-yandex-disk.sh >> /var/log/jeb/jeb.log" >> /tmp/jeb.cron
crontab /tmp/jeb.cron
