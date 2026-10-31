from ssh_lab import ROOT,connect,run
import json
c=connect()
try:
    r=run(c,'hostname; systemctl is-active nginx; systemctl is-enabled nginx; systemctl is-active unmsm-backup.timer; ip -br address; curl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1/; getent ahostsv4 archive.ubuntu.com | head -n 1')
    (ROOT/'evidencias/reinicio.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(r['output'])
finally:c.close()
