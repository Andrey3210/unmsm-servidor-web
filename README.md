# Implementación y administración de un servidor web

**Autor:** Andrey Hegel Zafra Venegas  
**Curso:** Taller de Construcción de Software Web  
**Universidad:** Universidad Nacional Mayor de San Marcos

Implementé una página de presentación de la UNMSM y la publiqué en una máquina virtual con Ubuntu Server y Nginx. El diseño toma como referencia los tonos granate y dorado, el encabezado institucional y las fotografías del [portal oficial](https://www.unmsm.edu.pe/).

## Enlaces

- Sitio de presentación: https://Andrey3210.github.io/unmsm-servidor-web/
- Repositorio: https://github.com/Andrey3210/unmsm-servidor-web
- Servidor del laboratorio: http://127.0.0.1:8088/ (con la VM encendida).

GitHub Pages aloja una copia estática para que se pueda revisar la página sin depender de mi computadora. Las pruebas de administración corresponden a Ubuntu Server con Nginx, no a GitHub Pages.

## Qué incluye el proyecto

El [informe técnico en PDF](informe/Informe_Servidor_Web_UNMSM_APA7.pdf) desarrolla las diez indicaciones, incluye 15 figuras y responde las cinco preguntas de análisis. Se presenta como trabajo estudiantil en APA 7, con referencias, sangría francesa y capturas explicadas. También se conserva una [fuente editable en Markdown](informe/Informe_Servidor_Web_UNMSM_APA7.md).

| Carpeta | Contenido |
| --- | --- |
| `dist/` | HTML, CSS, JavaScript e imágenes locales del sitio |
| `infra/` | Configuración de Nginx, aprovisionamiento, permisos, respaldo y comprobaciones |
| `evidencias/` | Capturas, configuración de VirtualBox y resultados reales de las pruebas |
| `informe/` | Informe técnico en PDF y su fuente editable |

## Entorno que utilicé

- VirtualBox 7.0.26, máquina `UNMSM-Web-Lab`.
- Ubuntu Server 24.04.5 LTS, kernel 6.8.0-147-generic.
- 1 procesador virtual, 2048 MB de RAM y disco de 20 GB.
- Nombre del servidor: `web-unmsm`.
- IPv4 estática: `10.0.2.15/24`; puerta de enlace: `10.0.2.2`.
- DNS operativo en la red del laboratorio: `192.168.18.1`.
- NAT: `127.0.0.1:8088` hacia el puerto 80 y `127.0.0.1:22022` hacia el puerto 22.
- Nginx 1.24.0, paquete Ubuntu `1.24.0-2ubuntu7.19`.

## Ejecutar solamente la página

Desde la carpeta del proyecto:

```bash
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Abrir `http://127.0.0.1:8000/`. Esto sirve para revisar el diseño; no reemplaza la instalación de Nginx de la práctica.

## Reproducir el servidor en Ubuntu

1. Crear una VM con Ubuntu Server de 64 bits, 2 GB de RAM y un disco de 20 GB.
2. Configurar la red según el entorno. Si se usa NAT de VirtualBox, crear las redirecciones indicadas arriba. El DNS debe ajustarse a la red disponible.
3. Configurar el nombre e instalar los paquetes:

```bash
sudo hostnamectl set-hostname web-unmsm
sudo apt-get update
sudo apt-get install -y nginx acl curl ufw
```

4. Copiar las carpetas `dist` e `infra` a `/home/andrey/lab/` dentro de la VM. El guion presupone un usuario administrador llamado `andrey`; adaptar las rutas si se utiliza otro nombre.
5. Ejecutar:

```bash
bash /home/andrey/lab/infra/administrar.sh
sudo nginx -t
systemctl is-active nginx
curl -I http://127.0.0.1/
```

El guion crea `editorweb` y el grupo `webeditors`, publica el contenido en `/var/www/unmsm/public`, configura Nginx, habilita UFW y programa una copia diaria a las 02:00.

Los guiones auxiliares de Python requieren `python -m pip install -r infra/requirements.txt`. Para automatizar la VM, `preparar_seed.py` crea un disco NoCloud y una clave local; `crear_vm.ps1` registra una máquina nueva a partir del VDI y el disco de configuración. Debe ejecutarse solamente cuando no exista ya una VM con ese nombre. El DNS de `preparar_seed.py` se adapta a la red antes de generar el disco.

La imagen oficial se obtiene de https://cloud-images.ubuntu.com/noble/current/ y se comprueba con `SHA256SUMS`. El disco original se convierte mediante `VBoxManage clonemedium disk ORIGINAL.vmdk ubuntu-lab.vdi --format VDI` y se amplía con `VBoxManage modifymedium disk ubuntu-lab.vdi --resize 20480`. No se incluyen los discos binarios en Git para evitar archivos de gran tamaño; la máquina utilizada para las pruebas queda registrada localmente en VirtualBox.

## Permisos que apliqué

El propietario del sitio es `root` y el grupo es `webeditors`. Los directorios utilizan `2775`, de modo que conservan el grupo en los nuevos elementos, y los archivos iniciales utilizan `664`. Las ACL permiten leer al proceso `www-data` sin darle escritura. `editorweb` no pertenece a `sudo`; su contraseña queda bloqueada y las pruebas se realizan mediante `sudo -u editorweb` desde la cuenta administradora.

La cuenta administrativa del aprovisionamiento usa una clave SSH y `sudo` sin contraseña en este laboratorio aislado. Las claves privadas y discos de la VM no forman parte del repositorio.

## Monitoreo y registros

```bash
uptime
top -b -n 1
free -h
df -h /
sudo tail /var/log/nginx/unmsm_access.log
sudo tail /var/log/nginx/unmsm_error.log
sudo journalctl -u nginx
```

## Copia y restauración

```bash
sudo /usr/local/sbin/backup-unmsm
systemctl list-timers unmsm-backup.timer
```

Las copias se guardan en `/var/backups/unmsm/`, con un archivo SHA-256. Comprobé la integridad y extraje el contenido a un directorio temporal; `diff -rq` no encontró diferencias respecto del sitio original. El respaldo incluye los archivos publicados y la configuración del sitio Nginx. Es una copia local de laboratorio; un entorno de producción también necesita una copia externa y una política de retención.

## Comprobaciones realizadas

- Configuración válida con `nginx -t`.
- Servicio activo y habilitado al iniciar.
- Respuesta HTTP 200 de la portada, 404 de una ruta inexistente y 403 de una ruta oculta.
- Edición permitida a `editorweb` y escritura denegada a `www-data`.
- Configuración de Nginx protegida frente a `editorweb`.
- Consulta de CPU, memoria, disco y registros.
- Verificación del respaldo por SHA-256 y comparación de los archivos restaurados.
- Navegación de escritorio y menú móvil en un marco de 390 px.
- Persistencia del sitio, la dirección y el temporizador después de reiniciar Ubuntu.

Los resultados completos están en `evidencias/resultados.json`. Las capturas administrativas muestran un visor de esas transcripciones SSH reales; las capturas del sitio y de la consola de Ubuntu corresponden a sus interfaces.

## Publicar en GitHub Pages

En la configuración del repositorio, abrir **Pages**, elegir la rama `main` y la carpeta `/docs`. La carpeta `docs/` es la copia de publicación de `dist/`. Si cambia la web, actualizar ambas carpetas antes de subir los cambios.

## Recursos gráficos

Las imágenes, el escudo y el fondo del encabezado proceden del portal oficial de la UNMSM. Se conservan sus derechos institucionales. Esta página es un proyecto académico de presentación y enlaza a los servicios oficiales; no recibe credenciales ni reemplaza el portal institucional.

## Guías consultadas para el informe

- [Guía oficial de configuración de un trabajo estudiantil APA 7](https://apastyle.apa.org/instructional-aids/student-paper-setup-guide.pdf).
- [Portada estudiantil](https://apastyle.apa.org/style-grammar-guidelines/paper-format/title-page).
- [Tablas y figuras](https://apastyle.apa.org/style-grammar-guidelines/tables-figures).

El documento utiliza Times New Roman de 12 puntos, márgenes de 2.54 cm, doble espacio en el cuerpo y las referencias, sangría inicial de 1.27 cm y números de página en la parte superior derecha. Los bloques de código y las notas de figuras se ajustan para mantener su legibilidad.
