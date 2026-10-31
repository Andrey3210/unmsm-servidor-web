"""Genera el informe estudiantil con formato APA 7 y las capturas verificadas."""
from pathlib import Path
import json,html,re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,KeepTogether,Preformatted,Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'informe/Informe_Servidor_Web_UNMSM_APA7.pdf'
for name,file in [('TimesAPA','times.ttf'),('TimesAPA-Bold','timesbd.ttf'),('TimesAPA-Italic','timesi.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('TimesAPA',normal='TimesAPA',bold='TimesAPA-Bold',italic='TimesAPA-Italic',boldItalic='TimesAPA-Bold')
styles={
 'p':ParagraphStyle('p',fontName='TimesAPA',fontSize=12,leading=24,firstLineIndent=36,spaceBefore=0,spaceAfter=0,alignment=TA_LEFT),
 'flat':ParagraphStyle('flat',fontName='TimesAPA',fontSize=12,leading=24,spaceBefore=0,spaceAfter=0),
 'h1':ParagraphStyle('h1',fontName='TimesAPA-Bold',fontSize=12,leading=24,alignment=TA_CENTER,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='TimesAPA-Bold',fontSize=12,leading=24,keepWithNext=True),
 'center':ParagraphStyle('center',fontName='TimesAPA',fontSize=12,leading=24,alignment=TA_CENTER),
 'caption':ParagraphStyle('caption',fontName='TimesAPA-Italic',fontSize=12,leading=24),
 'note':ParagraphStyle('note',fontName='TimesAPA',fontSize=10,leading=14,spaceAfter=12),
 'ref':ParagraphStyle('ref',fontName='TimesAPA',fontSize=12,leading=24,leftIndent=36,firstLineIndent=-36,splitLongWords=True),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8.5,leading=12,spaceBefore=6,spaceAfter=8),
}
story=[];source=[];fig=0
def para(text,style='p'):
    story.append(Paragraph(text,styles[style]));source.append(re.sub('<[^>]+>','',text)+'\n')
def heading(text,level=1):para(text,'h1' if level==1 else 'h2')
def code(text):
    story.append(Preformatted(text,styles['code'],maxLineLength=90));source.append('```bash\n'+text+'\n```\n')
def page():story.append(PageBreak())
def figure(file,title,note,maxh=400):
    global fig
    fig+=1;path=ROOT/'evidencias'/file
    w,h=PILImage.open(path).size; scale=min(468/w,maxh/h)
    items=[Paragraph(f'<b>Figura {fig}</b>',styles['flat']),Paragraph(title,styles['caption']),Image(str(path),width=w*scale,height=h*scale,hAlign='LEFT'),Paragraph('<i>Nota.</i> '+note,styles['note'])]
    story.append(KeepTogether(items));source.append(f'Figura {fig}. {title}\n\n![{title}](../evidencias/{file})\n\nNota. {note}\n')

TITLE='Implementación y administración de un servidor web con Ubuntu Server y Nginx'
class LogoInstitucional(Flowable):
    def __init__(self):
        Flowable.__init__(self)
        self.width=250
        self.height=80
        self.hAlign='CENTER'
    def draw(self):
        self.canv.setFillColorRGB(112/255,39/255,38/255)
        self.canv.rect(0,0,self.width,self.height,fill=1,stroke=0)
        self.canv.drawImage(ImageReader(str(ROOT/'informe/logo_unmsm.png')),20,12,width=210,height=56,mask='auto')
story.append(Spacer(1,18));story.append(LogoInstitucional());story.append(Spacer(1,24))
para(TITLE,'h1');story.append(Spacer(1,24))
for text in ['Andrey Hegel Zafra Venegas', 'Luis Guillermo Quispe Alvarado', 'Estefano Alexis Ramirez Garcia', 'Maleck Adriano Ramirez Alvarez', 'Joselin Victoria Gutierrez Mamani','Grupo 7','Facultad de Ingeniería de Sistemas e Informática','Universidad Nacional Mayor de San Marcos','Taller de Construcción de Software Web','31 de octubre de 2026']:
    para(text,'center')
page();heading(TITLE)
para('En esta práctica implementamos un servidor web para publicar una página de presentación de la Universidad Nacional Mayor de San Marcos (UNMSM). Nuestro propósito fue comprobar el ciclo de administración del servicio: preparar el sistema operativo, configurar la red, publicar contenido, separar permisos, supervisar recursos, revisar registros y recuperar archivos desde una copia de seguridad.')
para('Tomamos el portal institucional como referencia para la identidad visual y los enlaces de los servicios universitarios (Universidad Nacional Mayor de San Marcos [UNMSM], s. f.). La página del laboratorio conserva una estructura propia y utiliza recursos locales para que las imágenes y estilos no dependan de solicitudes externas durante su consulta.')
para('El resultado comprende dos entornos. El primero es una máquina virtual real con Ubuntu Server y Nginx, donde ejecutamos las pruebas administrativas. El segundo es una copia estática publicada en GitHub Pages para facilitar la revisión mediante un enlace público. La publicación externa no reemplaza la evidencia del servidor Linux.')
heading('Objetivo y alcance',2)
para('Nuestro objetivo general fue instalar, configurar y administrar un servidor web básico con Ubuntu Server y Nginx, aplicando procedimientos de supervisión, seguridad y mantenimiento. Para comprobarlo, seguimos las diez indicaciones de la actividad y respondimos sus cinco preguntas de análisis.')
para('La solución publica contenido HTML, CSS y JavaScript. La actividad no exige una base de datos ni un sistema de autenticación, por lo que mantuvimos el alcance en la presentación de la universidad y en la administración del servidor. No implementamos formularios que reciban contraseñas institucionales.')
heading('Entorno y arquitectura')
para('Creamos la máquina UNMSM-Web-Lab en VirtualBox 7.0.26. Utilizamos Ubuntu Server 24.04.5 LTS de 64 bits, 2048 MB de memoria, un procesador virtual y un disco de 20 GB. El sistema identificó el kernel Linux 6.8.0-147-generic y la plataforma de virtualización Oracle.')
para('Configuramos la interfaz enp0s3 con la dirección estática 10.0.2.15/24 y la puerta de enlace 10.0.2.2. La red NAT de VirtualBox permite la salida del invitado. Para consultar el sitio desde Windows, redirigimos 127.0.0.1:8088 al puerto 80 de la VM; para la administración SSH, redirigimos 127.0.0.1:22022 al puerto 22. Ambos accesos del anfitrión están ligados a la interfaz de bucle local.')
code('Navegador de Windows\n  http://127.0.0.1:8088\n       | NAT de VirtualBox\n       v\n  10.0.2.15:80 -> Nginx -> /var/www/unmsm/public\n\nAdministración: SSH 127.0.0.1:22022 -> 10.0.2.15:22\nPublicación externa: GitHub Pages -> copia estática en docs/')
heading('Creación de la máquina virtual e instalación de Ubuntu Server')
para('Preparamos Ubuntu a partir de una imagen oficial de servidor en formato VMDK. Verificamos su SHA-256 contra el archivo de sumas publicado por Canonical y después clonamos la imagen a un disco VDI de trabajo. De esta manera conservamos el archivo original y administramos una instalación independiente. La imagen utilizada fue noble-server-cloudimg-amd64.vmdk (Canonical, s. f.-c).')
code('SHA-256 verificado:\n9a1e3959c9f4ad9d4752101fd4ff9a43191fb7d72e61fa20e033f9fd235ce794')
para('El aprovisionamiento inicial se realizó con cloud-init y un disco NoCloud denominado seed.iso. Incluimos user-data, meta-data y network-config para establecer el usuario administrador, el nombre del equipo, la red y los paquetes. NoCloud permite entregar esta configuración desde un medio local (Canonical, s. f.-b). No utilizamos el asistente interactivo del instalador ISO; la instalación se desplegó a partir de la imagen oficial de Ubuntu Server.')
para('Durante el arranque inicial apareció un bloqueo relacionado con los temporizadores virtuales. Lo resolvimos dejando un procesador, habilitando HPET y manteniendo IO-APIC y el proveedor de paravirtualización predeterminado. Después del ajuste, Ubuntu completó el arranque y mostró el nombre web-unmsm, como se observa en la Figura 1.')
figure('01-consola-ubuntu.png','Consola de Ubuntu Server en la máquina virtual','Captura directa de la pantalla de la VM después de arrancar. La administración posterior se realizó por SSH.',340)
heading('Configuración del nombre y la dirección de red')
para('Asignamos el nombre web-unmsm y comprobamos la identidad con hostnamectl. Utilizamos Netplan para conservar la dirección estática y la ruta predeterminada. La Figura 2 reúne el sistema operativo, las direcciones, la ruta y la distribución del disco obtenidos desde la VM.')
code('hostnamectl\nip -br address\nip route\nsudo cat /etc/netplan/50-cloud-init.yaml\nsudo netplan generate')
para('La dirección DNS inicial de NAT, 10.0.2.3, no resolvía los nombres de los repositorios en este entorno. Probamos el servidor DNS de la red local, 192.168.18.1, y comprobamos la resolución de archive.ubuntu.com y una respuesta HTTP 200. Guardamos ese valor en Netplan. En otra red este DNS debe adaptarse; no corresponde copiarlo sin verificar que esté disponible.')
figure('01-sistema.png','Identidad del servidor, dirección estática y disco','Captura del visor de resultados de una sesión SSH real. La transcripción íntegra está en evidencias/resultados.json.',420)
heading('Instalación y configuración de Nginx')
para('Una vez corregida la resolución DNS, actualizamos el índice de paquetes e instalamos Nginx, ACL, curl y UFW mediante APT. El paquete instalado de Nginx fue 1.24.0-2ubuntu7.19. La documentación de Ubuntu describe la instalación del servidor desde los paquetes de la distribución (Canonical, s. f.-a).')
code('sudo apt-get update\nsudo apt-get install -y nginx acl curl ufw\nsudo systemctl enable --now nginx\nnginx -v\nsudo nginx -t')
para('Creamos /etc/nginx/sites-available/unmsm y lo habilitamos mediante un enlace en sites-enabled. Configuramos el puerto 80, la carpeta /var/www/unmsm/public y el archivo principal index.html. La directiva try_files devuelve 404 cuando el recurso no existe. La guía de Nginx explica el uso del bloque server, las ubicaciones y el directorio raíz para servir archivos estáticos (NGINX, s. f.).')
code('server {\n    listen 80 default_server;\n    server_name web-unmsm localhost 127.0.0.1;\n    root /var/www/unmsm/public;\n    index index.html;\n    location / { try_files $uri $uri/ =404; }\n}')
para('Antes de recargar el servicio ejecutamos nginx -t. El resultado indicó que la sintaxis era correcta y que la prueba fue satisfactoria. Después confirmamos active y enabled, además de la escucha en el puerto 80. La Figura 3 muestra estas comprobaciones; la configuración completa se encuentra en infra/unmsm.nginx.')
figure('02-nginx.png','Validación y estado del servicio Nginx','Salida real de nginx -t, systemctl y ss recogida mediante SSH.',400)
heading('Diseño y publicación de la página universitaria')
para('Organizamos la web en presentación, identidad institucional, oferta académica, investigación, comunidad y contacto. Tomamos como referencia el encabezado granate del portal oficial, sus detalles dorados y el contraste de títulos con tipografía serif. Utilizamos un fondo de la Ciudad Universitaria y fotografías de actividades académicas de la UNMSM. La Figura 4 presenta el portal consultado como referencia visual (UNMSM, s. f.).')
figure('00-referencia-oficial.png','Portal institucional utilizado como referencia visual','Captura de https://www.unmsm.edu.pe/, consultado el 31 de octubre de 2026. El portal y sus recursos gráficos pertenecen a la UNMSM.',310)
para('Implementamos el sitio con HTML semántico, CSS y JavaScript sin un proceso de compilación. Separamos los estilos y el comportamiento en archivos externos, mantuvimos las imágenes en assets y añadimos textos alternativos, enlaces descriptivos, un acceso para saltar al contenido y estilos de foco visibles. En pantallas pequeñas, el menú se abre con un botón que actualiza aria-expanded y puede cerrarse con Escape.')
para('Copiamos los archivos a /var/www/unmsm/public y aplicamos permisos al contenido. La portada publicada en Nginx se observa en la Figura 5. El pie de página identifica el carácter académico del proyecto y los botones de servicios remiten a sus destinos oficiales.')
figure('09-web-inicio.png','Portada de la página publicada en Nginx','Captura del navegador al consultar http://127.0.0.1:8088/. Los recursos gráficos se sirven desde la VM.',320)
heading('Comprobación desde el navegador')
para('Abrimos la dirección del anfitrión en Chrome y comprobamos que aparecieran el título, el escudo, las imágenes y las secciones. Los ocho enlaces internos apuntaban a identificadores existentes y las cuatro etiquetas de imagen completaron su carga. En la vista de escritorio no se detectó desbordamiento horizontal y no se registraron errores ni advertencias en la consulta de consola realizada durante esa prueba.')
para('Probamos el enlace Oferta académica y comprobamos que desplazara la página hacia las cinco áreas de conocimiento, como se observa en la Figura 6. Además de la comprobación visual, utilizamos curl para verificar los códigos de respuesta y las cabeceras HTTP.')
figure('10-web-oferta.png','Navegación hacia la oferta académica','Captura del resultado de seleccionar el enlace de navegación en el sitio del laboratorio.',300)
code('curl -I http://127.0.0.1/\n# Resultado: HTTP/1.1 200 OK\ncurl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1/no-existe\n# Resultado: 404\ncurl -s -o /dev/null -w "%{http_code}\\n" http://127.0.0.1/.env\n# Resultado: 403')
para('La respuesta 200 confirmó que la portada fue atendida. La respuesta 404 demostró el manejo de una ruta inexistente. La respuesta 403 fue provocada de forma controlada para comprobar el bloqueo de archivos ocultos; no representa una caída del servidor. La Figura 7 muestra los tres resultados y las cabeceras aplicadas.')
figure('03-http.png','Respuestas HTTP y cabeceras del sitio','Transcripción real de las consultas curl ejecutadas dentro de Ubuntu.',360)
heading('Verificación del diseño móvil',2)
para('Para revisar la adaptación del diseño cargamos temporalmente el sitio en un marco de 390 por 780 píxeles dentro de Chrome. Comprobamos la legibilidad de la portada y abrimos el menú; el estado accesible cambió de contraído a expandido y aparecieron los enlaces de navegación. Las Figuras 8 y 9 muestran ambas vistas. Esta es una prueba de tamaño de pantalla en el navegador, no una prueba realizada en un teléfono físico.')
figure('11-web-movil.png','Vista de la página en un marco de 390 píxeles','La página real se carga en el marco de prueba. Los archivos auxiliares se retiraron del servidor después de la revisión.',320)
figure('12-menu-movil.png','Menú de navegación abierto en la vista móvil','Captura posterior a pulsar Menú. El botón actualiza su estado aria-expanded.',320)
heading('Creación del usuario adicional y asignación de permisos')
para('Creamos el grupo webeditors y el usuario editorweb para separar la edición del contenido de la administración del servidor. La cuenta editorweb recibió un directorio personal y una shell, pero no fue añadida a sudo. Conservamos su contraseña bloqueada y realizamos las pruebas de acceso desde la cuenta administradora con sudo -u editorweb.')
code('sudo groupadd -f webeditors\nsudo useradd -m -s /bin/bash -g webeditors editorweb\nsudo usermod -aG webeditors andrey\nsudo chown -R root:webeditors /var/www/unmsm/public\nsudo find /var/www/unmsm/public -type d -exec chmod 2775 {} +\nsudo find /var/www/unmsm/public -type f -exec chmod 664 {} +')
para('El permiso 2775 de los directorios incluye el bit setgid, para que los nuevos elementos conserven el grupo de edición. Los archivos iniciales tienen permiso 664. Aplicamos ACL de lectura y acceso a directorios para www-data y ACL predeterminadas para conservar el acceso del grupo. La propiedad de los archivos de configuración de Nginx quedó en root, fuera del alcance de edición del usuario adicional.')
para('Comprobamos tres situaciones. Primero, editorweb creó, leyó y eliminó un archivo de prueba dentro del sitio. Segundo, www-data no pudo escribir en el directorio publicado. Tercero, editorweb no pudo modificar la configuración de Nginx y sudo confirmó que no tenía autorización administrativa. La Figura 10 reúne los resultados de estas pruebas positivas y negativas.')
figure('04-permisos.png','Usuario editorweb y separación de permisos','La prueba controlada de escritura se retiró al terminar. La salida de sudo -l confirma que editorweb no puede ejecutar sudo.',430)
heading('Supervisión de CPU, memoria y disco')
para('Consultamos uptime, top, free, df y ps para observar el estado del servidor. En la medición de las 10:47:36, el sistema mostró aproximadamente 301 MiB de memoria utilizada y 1.6 GiB disponibles. La partición raíz utilizaba 1.9 GiB de 19 GiB, equivalente al 11 %. El contenido publicado ocupaba aproximadamente 1.5 MiB. La Figura 11 conserva la medición completa.')
code('uptime\ntop -b -n 1 | head -n 12\nfree -h\ndf -h /\ndu -sh /var/www/unmsm/public\nps -C nginx -o pid,user,%cpu,%mem,cmd')
para('La primera muestra de top reportó 88.9 % de CPU inactiva. Esta cifra es una observación puntual del laboratorio y no una prueba de capacidad bajo carga. El promedio de carga de un minuto fue 0.82 en una VM con un procesador. Los valores deben interpretarse junto con su evolución, porque una instalación reciente o una tarea de mantenimiento pueden elevar temporalmente la carga.')
para('Identificamos el proceso maestro de Nginx con root y el proceso trabajador con www-data. Esta separación permite que el proceso que atiende las solicitudes no tenga permisos de escritura sobre los archivos publicados. Para una operación continua estableceríamos alertas de memoria disponible, espacio de disco, carga sostenida y errores del servicio; en esta práctica realizamos la inspección manual de esos indicadores.')
figure('05-recursos.png','Consumo de CPU, memoria, disco y procesos de Nginx','Medición real de la VM el 31 de octubre de 2026. No corresponde a un ensayo de rendimiento ni a una serie histórica.',410)
heading('Revisión de registros de actividad')
para('Configuramos un registro de acceso específico, /var/log/nginx/unmsm_access.log, y un registro de errores, /var/log/nginx/unmsm_error.log. También consultamos journalctl para revisar los eventos de inicio y recarga del servicio. La Figura 12 muestra las solicitudes controladas y los eventos administrativos.')
code('sudo tail -n 8 /var/log/nginx/unmsm_access.log\nsudo tail -n 5 /var/log/nginx/unmsm_error.log\nsudo journalctl -u nginx -n 5 --no-pager')
para('En access.log identificamos la fecha y la hora, el método HTTP, la ruta, el protocolo, el código de respuesta y el agente de usuario. Las solicitudes de la portada generaron 200, la ruta /no-existe generó 404 y /.env generó 403. El error access forbidden by rule coincidió con la prueba de archivo oculto, por lo que pudimos relacionar el registro con una acción conocida.')
para('La consulta de journalctl mostró que Nginx había iniciado y que la configuración se había recargado correctamente. Revisar los registros resulta útil para distinguir una falla de sintaxis, un problema de permisos y una solicitud inválida. La presencia de una entrada de error aislada no demuestra por sí misma que el servicio completo esté detenido.')
figure('06-registros.png','Registros de acceso, rechazo controlado y eventos del servicio','La solicitud a /.env fue generada para probar la regla de bloqueo; no se publicó ningún archivo de credenciales.',390)
heading('Copia de seguridad y restauración de prueba')
para('Implementamos el guion /usr/local/sbin/backup-unmsm para respaldar /var/www/unmsm y /etc/nginx/sites-available/unmsm. La copia utiliza tar con compresión gzip y la opción --acls. El directorio /var/backups/unmsm tiene acceso restringido y umask 077 limita la lectura de los archivos nuevos al propietario.')
code('sudo /usr/local/sbin/backup-unmsm\n# Ejemplo de archivo creado:\n# /var/backups/unmsm/unmsm-20261031-104736.tar.gz\n# Se genera también un archivo .sha256')
para('No nos limitamos a comprobar que existiera el archivo. Validamos la suma SHA-256, extrajimos el respaldo en una carpeta temporal y comparamos el contenido restaurado con el sitio original mediante diff -rq. La suma devolvió OK y la comparación terminó sin diferencias. La Figura 13 presenta la evidencia; la prueba verificó el contenido, mientras que la opción --acls se incluyó para conservar la información de permisos en el archivo.')
code('cd /var/backups/unmsm\nsudo sha256sum -c unmsm-20261031-104736.tar.gz.sha256\n# Extracción de prueba en un directorio temporal:\nsudo tar --acls -xzpf ARCHIVO.tar.gz -C DIRECTORIO_TEMPORAL\nsudo diff -rq /var/www/unmsm/public \\\n    DIRECTORIO_TEMPORAL/var/www/unmsm/public')
para('Programamos la ejecución diaria a las 02:00 mediante un servicio y un temporizador de systemd. Persistent=true permite ejecutar una copia pendiente después de volver a encender la máquina. El respaldo del laboratorio es local; no protege frente a la pérdida completa del disco virtual. Para un servicio real añadiríamos almacenamiento externo, retención de versiones y restauraciones periódicas.')
figure('08-respaldo.png','Validación de integridad y restauración del respaldo','La salida RESTAURACION_VERIFICADA_SIN_DIFERENCIAS se emite únicamente después de que sha256sum y diff finalizan correctamente.',370)
heading('Medidas de seguridad y mantenimiento')
para('Habilitamos UFW después de autorizar OpenSSH y Nginx HTTP. La política observada fue denegar conexiones entrantes no permitidas y aceptar las salientes. Dentro de la VM se admiten los puertos 22 y 80; la publicación de estos puertos en Windows continúa limitada a 127.0.0.1 por la configuración NAT. La Figura 14 muestra el firewall activo y la copia programada.')
code("sudo ufw allow OpenSSH\nsudo ufw allow 'Nginx HTTP'\nsudo ufw --force enable\nsudo ufw status verbose\nsystemctl list-timers unmsm-backup.timer")
para('Deshabilitamos el listado de directorios y la exposición de la versión de Nginx, bloqueamos las rutas ocultas y añadimos cabeceras X-Content-Type-Options, Referrer-Policy, X-Frame-Options y Content-Security-Policy. El sitio utiliza sus propios archivos de estilos, scripts e imágenes, por lo que la política de contenido permite limitar estos recursos al mismo origen. El acceso HTTP del laboratorio no cuenta con un certificado TLS; la copia pública de GitHub Pages se consulta mediante HTTPS.')
figure('07-seguridad.png','Firewall activo y programación de la copia diaria','La consulta del temporizador muestra la siguiente ejecución prevista para las 02:00 del día siguiente.',370)
para('Reiniciamos Ubuntu y volvimos a consultar el nombre, la dirección y los servicios. Nginx quedó active y enabled, el temporizador quedó active, la interfaz mantuvo 10.0.2.15/24 y curl devolvió 200. Guardamos esta comprobación en evidencias/reinicio.json. Esto demuestra la persistencia de la configuración tras un reinicio; no constituye una prueba de tolerancia a fallos de infraestructura.')
heading('Publicación del proyecto y enlace de revisión')
para('Publicamos el código fuente en el repositorio Andrey3210/unmsm-servidor-web. Organizamos dist como fuente del sitio, infra para la configuración y los guiones, evidencias para los resultados e informe para el documento técnico. Excluimos las claves privadas, los discos virtuales y los archivos de ejecución que no forman parte de la entrega.')
para('Configuramos GitHub Pages para publicar desde la rama main y la carpeta /docs, que contiene una copia de los archivos del sitio. Este procedimiento coincide con las opciones de publicación documentadas por GitHub (s. f.). La finalidad de este segundo despliegue es que el profesor pueda revisar la página sin depender de que la VM del laboratorio permanezca encendida.')
para('Sitio público: <link href="https://andrey3210.github.io/unmsm-servidor-web/">https://andrey3210.github.io/unmsm-servidor-web/</link>', 'flat')
para('Repositorio: <link href="https://github.com/Andrey3210/unmsm-servidor-web">https://github.com/Andrey3210/unmsm-servidor-web</link>', 'flat')
if (ROOT/'evidencias/14-web-publica.png').exists():
    para('La Figura 15 muestra la portada consultada en el enlace público después de completar el despliegue.')
    figure('14-web-publica.png','Página disponible mediante GitHub Pages','Captura del sitio público. Las pruebas de usuarios, permisos, recursos y respaldos corresponden al servidor Ubuntu del laboratorio.',310)
heading('Respuestas a las preguntas de análisis')
heading('¿Por qué es importante supervisar permanentemente los servidores?',2)
para('La supervisión permite detectar condiciones que pueden interrumpir el servicio antes de que afecten a todos los usuarios. Por ejemplo, un disco cercano a su capacidad puede impedir la escritura de registros, mientras que una reducción sostenida de memoria disponible puede generar lentitud o terminar procesos. Un servicio puede continuar respondiendo durante una degradación inicial, por lo que observar únicamente si la portada abre resulta insuficiente.')
para('En la práctica comprobamos CPU, memoria, disco, procesos y estado de Nginx. Para una supervisión permanente complementaríamos estas consultas con mediciones históricas y alertas. También diferenciaríamos una variación puntual de un problema sostenido: una muestra de CPU durante una actualización no demuestra que el servidor sea incapaz de atender solicitudes.')
heading('¿Qué consecuencias puede ocasionar una mala administración de permisos?',2)
para('Un exceso de permisos permite que una cuenta de edición modifique configuraciones sensibles o que una vulnerabilidad en el servicio altere el contenido publicado. Un acceso insuficiente también produce problemas: si el proceso trabajador no puede leer index.html, una página válida puede devolver un error. Por eso, la configuración debe permitir las operaciones necesarias y denegar las demás.')
para('La prueba con editorweb confirmó que se puede delegar la modificación del contenido sin conceder sudo ni escritura sobre Nginx. La prueba con www-data verificó que el proceso del servicio puede atender archivos sin poder modificarlos. Aplicar permisos 777 habría eliminado esa separación y ampliado innecesariamente las posibilidades de alteración del sitio.')
heading('¿Qué sucede cuando un servidor web deja de funcionar?',2)
para('Los usuarios pierden el acceso al contenido o reciben errores de conexión. El mensaje concreto depende del punto de falla: si Nginx está detenido, la conexión puede ser rechazada; si un intermediario no alcanza al servidor de origen, puede devolver un error de puerta de enlace; si solo falta un archivo, puede aparecer 404 sin que todo el servidor haya caído. La consecuencia funcional es la interrupción parcial o total de los servicios que dependen de esa publicación.')
para('Para investigar una interrupción revisaríamos primero el estado de systemd, después la sintaxis de Nginx, la escucha del puerto, la red y los registros. No reiniciaríamos repetidamente sin revisar la causa. En esta práctica no provocamos una caída deliberada de Nginx; comprobamos su recuperación automática después de reiniciar la VM y diferenciamos las respuestas 403 y 404 de una indisponibilidad general.')
heading('¿Por qué es necesario realizar copias de seguridad?',2)
para('Las copias permiten recuperar archivos ante una eliminación accidental, una modificación incorrecta o una pérdida del sistema. El código del sitio y la configuración del servidor forman una unidad de recuperación: restaurar únicamente index.html no reconstruye necesariamente el servicio. Además, un archivo comprimido que nunca se ha probado puede resultar incompleto o inutilizable cuando se necesita.')
para('Por ese motivo respaldamos el contenido y la configuración, calculamos SHA-256 y realizamos una extracción de prueba. La comparación sin diferencias demuestra que ese respaldo concreto contenía los archivos esperados. Para una protección mayor mantendríamos copias fuera de la VM y definiríamos cuánto tiempo conservarlas, cuánto dato es aceptable perder y cuánto debe tardar la recuperación.')
heading('¿Qué ventajas ofrece administrar servidores de manera remota?',2)
para('La administración remota permite revisar y mantener un servidor sin estar frente a su consola física. Una conexión SSH facilita consultar registros, transferir archivos y ejecutar procedimientos repetibles. En este laboratorio administramos Ubuntu desde Windows a través de una redirección local, lo que permitió documentar comandos y resultados sin instalar un escritorio gráfico en el servidor.')
para('También mejora la trazabilidad cuando se conservan las transcripciones y se utilizan cuentas diferenciadas. Estas ventajas requieren proteger el acceso: mantuvimos autenticación por clave para la cuenta administradora y no publicamos el puerto SSH en Internet. La cuenta editorweb quedó separada de las funciones administrativas. La comodidad del acceso remoto no justifica conceder privilegios amplios a todos los usuarios.')
heading('Incidencias y decisiones adoptadas')
para('La primera incidencia fue un bloqueo del kernel durante el arranque de VirtualBox. Conservamos la imagen oficial verificada y ajustamos los temporizadores virtuales y el número de procesadores. La configuración final utiliza un procesador, HPET habilitado, IO-APIC habilitado y el proveedor de paravirtualización predeterminado. No fue necesario modificar el kernel de Ubuntu.')
para('La segunda incidencia fue la resolución DNS del invitado. cloud-init registró un error durante su primer intento de instalar paquetes. Corregimos el DNS en Netplan y completamos la actualización e instalación con APT. El estado histórico de cloud-init conserva ese fallo inicial; por ello verificamos el resultado efectivo con dpkg-query, nginx -t, systemctl, curl y una prueba posterior al reinicio, en lugar de afirmar que el aprovisionamiento inicial no había tenido errores.')
para('La tercera decisión fue separar el enlace público de la infraestructura administrativa. GitHub Pages permite revisar el diseño, pero no ejecuta las cuentas, los permisos ni los respaldos de la VM. Las evidencias del informe identifican cuál entorno se está comprobando en cada caso para evitar atribuir a GitHub Pages resultados obtenidos en Ubuntu.')
heading('Conclusiones')
para('Implementamos una máquina virtual con Ubuntu Server, una dirección estática y un servidor Nginx que publica la página de presentación de la UNMSM. Comprobamos su acceso desde el navegador y mediante HTTP, y verificamos que Nginx y la dirección permanecieran configurados después de reiniciar el sistema.')
para('La separación entre root, webeditors, editorweb y www-data permitió delegar la edición del contenido sin conceder administración del servidor. Las pruebas positivas y negativas demostraron los permisos efectivos, más allá de la lectura de sus valores numéricos.')
para('La revisión de recursos y registros permitió relacionar el estado del sistema con las solicitudes de prueba. La creación de un respaldo, la verificación de su suma y la comparación de los archivos restaurados cerraron el ciclo básico de mantenimiento. La copia local y la supervisión puntual satisfacen el alcance del laboratorio, aunque una operación de producción requiere respaldo externo, retención y monitoreo continuo.')
para('El repositorio conserva los archivos del proyecto y las instrucciones para reproducirlo. La publicación estática ofrece un enlace de revisión independiente del equipo del laboratorio, mientras que las capturas y transcripciones documentan la administración real de Ubuntu Server y Nginx.')
page();heading('Referencias')
references=[
'American Psychological Association. (s. f.). <i>Student paper setup guide</i>. https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf',
'Canonical. (s. f.-c). <i>Ubuntu 24.04 LTS (Noble Numbat) daily</i>. Ubuntu Cloud Images. Recuperado el 31 de octubre de 2026, de https://cloud-images.ubuntu.com/noble/current/',
'Canonical. (s. f.-a). <i>Install and configure Nginx</i>. Ubuntu. https://ubuntu.com/tutorials/install-and-configure-nginx',
'Canonical. (s. f.-b). <i>NoCloud</i>. cloud-init documentation. https://docs.cloud-init.io/en/26.1/reference/datasources/nocloud.html',
'GitHub. (s. f.). <i>Creating a GitHub Pages site</i>. GitHub Docs. https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site',
'NGINX. (s. f.). <i>Beginner’s guide</i>. https://nginx.org/en/docs/beginners_guide.html',
'Universidad Nacional Mayor de San Marcos. (s. f.). <i>Universidad Nacional Mayor de San Marcos</i>. Recuperado el 31 de octubre de 2026, de https://www.unmsm.edu.pe/',
]
references.sort(key=lambda x: x.casefold())
for ref in references:para(ref,'ref')
page();heading('Apéndice A');heading('Guía de reproducción y archivos de entrega')
para('Para reproducir el laboratorio, crearíamos una VM con Ubuntu Server de 64 bits, 2 GB de RAM y un disco de 20 GB. Configuraríamos la red y ajustaríamos el DNS al entorno disponible. Después instalaríamos nginx, acl, curl y ufw; copiaríamos dist e infra a /home/andrey/lab y ejecutaríamos administrar.sh. La ruta asume una cuenta administrativa llamada andrey y debe modificarse cuando se use otro nombre.')
code('sudo hostnamectl set-hostname web-unmsm\nsudo apt-get update\nsudo apt-get install -y nginx acl curl ufw\nbash /home/andrey/lab/infra/administrar.sh\nsudo nginx -t\nsystemctl is-active nginx\ncurl -I http://127.0.0.1/')
para('Los archivos principales son dist/index.html, dist/styles.css y dist/app.js; la configuración del servidor está en infra/unmsm.nginx. El guion infra/administrar.sh aplica el despliegue y los permisos, mientras que backup-unmsm.sh y las unidades unmsm-backup.service y unmsm-backup.timer implementan las copias. verificar.py conserva los resultados administrativos en JSON.')
para('Las capturas de los comandos se obtuvieron desde un visor de las transcripciones reales de SSH. Este visor mejora la lectura, pero no representa una consola interactiva. Los archivos resultados.json, reinicio.json y despliegue.json conservan los comandos, las salidas y sus códigos. La consola de Ubuntu y las páginas del navegador se capturaron directamente de sus interfaces.')
para('Para la presentación del documento utilizamos la guía oficial de trabajos estudiantiles de APA: márgenes de 2.54 cm, Times New Roman de 12 puntos, doble espacio en el texto, sangría de primera línea de 1.27 cm y numeración superior derecha. Las referencias utilizan sangría francesa; las figuras incluyen número, título y nota explicativa (American Psychological Association, s. f.).')
page();heading('Apéndice B');heading('Configuración completa del sitio Nginx')
para('La siguiente configuración corresponde al archivo instalado en sites-available. El sitio predeterminado de la VM fue sustituido por el enlace hacia esta configuración.')
code((ROOT/'infra/unmsm.nginx').read_text(encoding='utf-8'))

def header(canvas,doc):
    canvas.saveState();canvas.setFont('TimesAPA',12);canvas.drawRightString(540,756,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),leftMargin=72,rightMargin=72,topMargin=72,bottomMargin=72,title=TITLE,author='Andrey Hegel Zafra Venegas; Luis Guillermo Quispe Alvarado; Estefano Alexis Ramirez Garcia; Maleck Adriano Ramirez Alvarez; Joselin Victoria Gutierrez Mamani')
doc.build(story,onFirstPage=header,onLaterPages=header)
(ROOT/'informe/Informe_Servidor_Web_UNMSM_APA7.md').write_text('\n'.join(source),encoding='utf-8')
print(OUT)
