from ssh_lab import connect
c=connect()
try:
    s=c.open_sftp()
    with s.file('/home/andrey/responsive.html','w') as f:
        f.write('''<!doctype html><html lang="es"><meta charset="utf-8"><title>Prueba de diseño móvil a 390 px</title><style>body{margin:0;background:#eeeae4;font-family:Arial;color:#382626;padding:30px;display:flex;gap:55px;justify-content:center}h1{font:36px Georgia;max-width:320px}p{max-width:320px;line-height:1.7;font-size:15px}iframe{width:390px;height:780px;border:8px solid #292727;border-radius:20px;background:white;box-shadow:0 15px 40px #0002}small{display:block;color:#666;max-width:320px}</style><section><p>VALIDACIÓN RESPONSIVE</p><h1>San Marcos en una pantalla de 390 px.</h1><p>La página real se carga en un marco de 390 × 780 píxeles. Se comprueban el menú, la lectura y el ajuste del contenido.</p><small>Prueba de laboratorio en Chrome. No corresponde a una captura de un teléfono físico.</small></section><iframe src="/" title="Vista móvil del sitio UNMSM"></iframe></html>''')
    with s.file('/home/andrey/responsive.html','r') as f: text=f.read().decode()
    css=text.split('<style>')[1].split('</style>')[0]
    text=text.replace('<style>'+css+'</style>','<link rel="stylesheet" href="/__qa.css">')
    with s.file('/home/andrey/responsive.html','w') as f:f.write(text)
    with s.file('/home/andrey/responsive.css','w') as f:f.write(css)
    s.close()
    _,out,err=c.exec_command('sudo install -m 644 /home/andrey/responsive.html /var/www/unmsm/public/__qa.html; sudo install -m 644 /home/andrey/responsive.css /var/www/unmsm/public/__qa.css');out.channel.recv_exit_status()
finally:c.close()
