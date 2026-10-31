#!/usr/bin/env bash
set -euo pipefail
# Ejecutar como administrador de la VM; archivos subidos previamente a /home/andrey/lab.
sudo groupadd -f webeditors
if ! id editorweb >/dev/null 2>&1; then sudo useradd --create-home --shell /bin/bash --gid webeditors editorweb; fi
sudo usermod -aG webeditors andrey
sudo install -d -o root -g webeditors -m 2775 /var/www/unmsm/public
sudo cp -a /home/andrey/lab/dist/. /var/www/unmsm/public/
sudo chown -R root:webeditors /var/www/unmsm/public
sudo find /var/www/unmsm/public -type d -exec chmod 2775 {} +
sudo find /var/www/unmsm/public -type f -exec chmod 664 {} +
sudo setfacl -R -m g:www-data:r-X /var/www/unmsm/public
sudo setfacl -R -d -m g:webeditors:rwX,g:www-data:r-X,o::r-X /var/www/unmsm/public
sudo install -o root -g root -m 644 /home/andrey/lab/infra/unmsm.nginx /etc/nginx/sites-available/unmsm
sudo ln -sfn /etc/nginx/sites-available/unmsm /etc/nginx/sites-enabled/unmsm
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx HTTP'
sudo ufw --force enable
sudo install -d -m 700 /var/backups/unmsm
sudo install -o root -g root -m 750 /home/andrey/lab/infra/backup-unmsm.sh /usr/local/sbin/backup-unmsm
sudo install -o root -g root -m 644 /home/andrey/lab/infra/unmsm-backup.service /etc/systemd/system/unmsm-backup.service
sudo install -o root -g root -m 644 /home/andrey/lab/infra/unmsm-backup.timer /etc/systemd/system/unmsm-backup.timer
sudo systemctl daemon-reload
sudo systemctl enable --now unmsm-backup.timer
sudo /usr/local/sbin/backup-unmsm
