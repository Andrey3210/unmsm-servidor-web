from ssh_lab import ROOT,connect,run
import json
commands=[
('01-sistema','Identidad, sistema operativo y red','hostnamectl; ip -br address; ip route; resolvectl status enp0s3 | head -n 14; lsblk -o NAME,SIZE,TYPE,MOUNTPOINTS'),
('02-nginx','Instalación y validación de Nginx','nginx -v; dpkg-query -W nginx nginx-common; sudo nginx -t; systemctl is-active nginx; systemctl is-enabled nginx; systemctl status nginx --no-pager | head -n 13; ss -ltn | grep -E ":(22|80) "'),
('03-http','Respuesta HTTP y cabeceras de seguridad','curl -sSI http://127.0.0.1/; printf "\\nTítulo publicado: "; curl -s http://127.0.0.1/ | grep -o "<title>[^<]*</title>"; printf "\\nRecurso inexistente: "; curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1/no-existe; printf "Archivo oculto: "; curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1/.env'),
('04-permisos','Usuario adicional y pruebas positivas y negativas','id editorweb; sudo passwd -S editorweb; stat -c "%A %U:%G %n" /var/www/unmsm/public /var/www/unmsm/public/index.html; getfacl -p /var/www/unmsm/public | head -n 18; sudo -u editorweb bash -c \'echo "prueba controlada" > /var/www/unmsm/public/prueba-permisos.txt && cat /var/www/unmsm/public/prueba-permisos.txt && rm /var/www/unmsm/public/prueba-permisos.txt\'; if sudo -u www-data test -w /var/www/unmsm/public; then echo "ERROR: www-data puede escribir"; exit 1; else echo "CORRECTO: www-data no puede escribir"; fi; if sudo -u editorweb test -w /etc/nginx/sites-available/unmsm; then echo "ERROR: editor modifica configuración"; exit 1; else echo "CORRECTO: editorweb no modifica Nginx"; fi; sudo -l -U editorweb'),
('05-recursos','Supervisión de CPU, memoria y disco','uptime; top -b -n 1 | head -n 12; free -h; df -h /; du -sh /var/www/unmsm/public; ps -C nginx -o pid,user,%cpu,%mem,cmd'),
('06-registros','Registros de actividad y errores','sudo tail -n 8 /var/log/nginx/unmsm_access.log; sudo tail -n 5 /var/log/nginx/unmsm_error.log; sudo journalctl -u nginx -n 5 --no-pager'),
('07-seguridad','Firewall y servicio de copia automática','sudo ufw status verbose; systemctl list-timers unmsm-backup.timer --no-pager; systemctl cat unmsm-backup.timer'),
('08-respaldo','Copia, integridad y restauración de prueba',"sudo bash -c 'set -e; /usr/local/sbin/backup-unmsm; cd /var/backups/unmsm; latest=$(ls -t *.tar.gz | head -n 1); sha256sum -c \"$latest.sha256\"; restore=$(mktemp -d /tmp/unmsm-restore.XXXXXX); tar --acls -xzpf \"$latest\" -C \"$restore\"; diff -rq /var/www/unmsm/public \"$restore/var/www/unmsm/public\"; echo RESTAURACION_VERIFICADA_SIN_DIFERENCIAS; ls -lh \"$latest\" \"$latest.sha256\"; printf \"Directorio de prueba: %s\\n\" \"$restore\"; tar -tzf \"$latest\" | head -n 12'"),
]
c=connect(); results=[]
try:
    for slug,title,cmd in commands:
        r=run(c,cmd);r.update(slug=slug,title=title);results.append(r)
        print(slug,r['exit_code'])
    (ROOT/'evidencias/resultados.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    s=c.open_sftp();r=run(c,"sudo bash -c 'cp $(ls -t /var/backups/unmsm/*.tar.gz | head -n 1) /home/andrey/respaldo-unmsm.tar.gz; chown andrey:andrey /home/andrey/respaldo-unmsm.tar.gz'")
    s.get('/home/andrey/respaldo-unmsm.tar.gz',str(ROOT/'evidencias/respaldo-unmsm.tar.gz'));s.close()
finally:c.close()
if any(r['exit_code'] for r in results):raise SystemExit('Revisar comandos con error')
