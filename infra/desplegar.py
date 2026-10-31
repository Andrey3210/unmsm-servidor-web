from ssh_lab import ROOT,connect,run
import json,posixpath
c=connect()
try:
    status=run(c,'cloud-init status --wait')
    print(json.dumps(status,ensure_ascii=False))
    # El primer aprovisionamiento registró un error DNS; se corrigió Netplan
    # y se completó APT manualmente. Verificar el paquete real antes de seguir.
    ready=run(c,'dpkg-query -W -f=\'${Status}\' nginx')
    if 'install ok installed' not in ready['output']:raise RuntimeError('Nginx no está instalado')
    s=c.open_sftp()
    def mkdir(path):
        try:s.mkdir(path)
        except IOError:pass
    mkdir('/home/andrey/lab')
    for folder in ('dist','infra'):
        mkdir('/home/andrey/lab/'+folder)
        files=(ROOT/folder).rglob('*') if folder=='dist' else (ROOT/folder).glob('*')
        for f in files:
            if not f.is_file() or (folder=='infra' and f.suffix not in ('.sh','.nginx','.service','.timer')):continue
            rel=f.relative_to(ROOT).as_posix();target='/home/andrey/lab/'+rel
            parts=target.split('/')[:-1]
            for i in range(2,len(parts)+1):mkdir('/'.join(parts[:i]))
            s.put(str(f),target)
    s.close()
    r=run(c,'bash /home/andrey/lab/infra/administrar.sh')
    (ROOT/'evidencias/despliegue.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))
    if r['exit_code']:raise RuntimeError('Falló el despliegue')
finally:c.close()
