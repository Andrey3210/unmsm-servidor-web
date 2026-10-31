# Crear una VM nueva a partir del VDI y seed.iso preparados en esta carpeta.
# No modifica otras máquinas registradas. Ejecutar desde PowerShell.
$ErrorActionPreference = 'Stop'
$vbox = 'C:/Program Files/Oracle/VirtualBox/VBoxManage.exe'
$nombre = 'UNMSM-Web-Lab'
$base = $PSScriptRoot
function Ejecutar-VBox {
    & $vbox @args
    if ($LASTEXITCODE -ne 0) { throw "VirtualBox devolvió un error: $args" }
}
if (-not (Test-Path -LiteralPath "$base/ubuntu-lab.vdi")) {
    throw 'Falta ubuntu-lab.vdi. Clonar la imagen oficial y ampliar el VDI a 20480 MB antes de continuar.'
}
if (-not (Test-Path -LiteralPath "$base/seed.iso")) {
    throw 'Falta seed.iso. Ejecutar primero python infra/preparar_seed.py.'
}
Ejecutar-VBox createvm --name $nombre --ostype Ubuntu_64 --basefolder "$base/vm" --register
Ejecutar-VBox modifyvm $nombre --memory 2048 --cpus 1 --ioapic on --hpet on --paravirtprovider default --nic1 nat --natpf1 'ssh,tcp,127.0.0.1,22022,,22' --natpf1 'web,tcp,127.0.0.1,8088,,80'
Ejecutar-VBox storagectl $nombre --name SATA --add sata --controller IntelAhci --portcount 2
Ejecutar-VBox storageattach $nombre --storagectl SATA --port 0 --device 0 --type hdd --medium "$base/ubuntu-lab.vdi"
Ejecutar-VBox storageattach $nombre --storagectl SATA --port 1 --device 0 --type dvddrive --medium "$base/seed.iso"
Ejecutar-VBox startvm $nombre --type headless
