from pathlib import Path
import sys, io
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tmp/lab-deps'))
import pycdlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
p=Path(__file__).resolve().parent
(p/'private').mkdir(exist_ok=True)
keyfile=p/'private/id_ed25519'
if not keyfile.exists():
    key=ed25519.Ed25519PrivateKey.generate()
    keyfile.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.OpenSSH,serialization.NoEncryption()))
    (p/'private/id_ed25519.pub').write_bytes(key.public_key().public_bytes(serialization.Encoding.OpenSSH,serialization.PublicFormat.OpenSSH))
pub=(p/'private/id_ed25519.pub').read_text()
user=f'''#cloud-config
hostname: web-unmsm
manage_etc_hosts: true
users:
  - name: andrey
    gecos: Administrador del laboratorio
    groups: [adm, sudo]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    lock_passwd: true
    ssh_authorized_keys:
      - {pub}
ssh_pwauth: false
disable_root: true
package_update: true
packages: [nginx, acl, curl, ufw]
timezone: America/Lima
runcmd:
  - [systemctl, enable, --now, nginx]
'''
meta='instance-id: unmsm-web-lab-20261031\nlocal-hostname: web-unmsm\n'
network='''version: 2
ethernets:
  enp0s3:
    match:
      name: "en*"
    dhcp4: false
    addresses: [10.0.2.15/24]
    routes:
      - to: default
        via: 10.0.2.2
    nameservers:
      addresses: [192.168.18.1]
'''
iso=pycdlib.PyCdlib(); iso.new(interchange_level=3,joliet=3,rock_ridge='1.09',vol_ident='cidata')
for name,data in [('user-data',user),('meta-data',meta),('network-config',network)]:
    b=data.encode(); iso.add_fp(io.BytesIO(b),len(b),iso_path='/'+name.upper().replace('-','_')+';1',rr_name=name,joliet_path='/'+name)
iso.write(str(p/'seed.iso')); iso.close()
print('Disco NoCloud creado. Clave SSH local conservada fuera del entregable.')
