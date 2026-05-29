# Proxmox Server - Komplette Installations- und Konfigurationsanleitung

## Inhaltsverzeichnis
- [Milestone I: Vorbereitung und Planung](#milestone-i-vorbereitung-und-planung)
- [Milestone II: Hardware-Vorbereitung und Proxmox Installation](#milestone-ii-hardware-vorbereitung-und-proxmox-installation)
- [Milestone III: Grundkonfiguration](#milestone-iii-grundkonfiguration)
- [Milestone IV: Netzwerk-Konfiguration](#milestone-iv-netzwerk-konfiguration)
- [Milestone V: Storage-Konfiguration](#milestone-v-storage-konfiguration)
- [Milestone VI: Erste VMs und Container](#milestone-vi-erste-vms-und-container)
- [Milestone VII: Absicherung und Monitoring](#milestone-vii-absicherung-und-monitoring)
- [Optional: Backup-Konfiguration](#optional-backup-konfiguration)
- [Optional: NIC2 für Management](#optional-nic2-für-management)

---

## Milestone I: Vorbereitung und Planung

### Ziel
Hardware-Anforderungen klären und Netzwerkplanung durchführen.

### Schritt-für-Schritt Anleitung

#### 1.1 Hardware-Anforderungen prüfen
- **Minimum:**
  - CPU: 64-bit Prozessor mit Intel VT/AMD-V Support
  - RAM: 4 GB (empfohlen: 8 GB+)
  - Festplatte: 32 GB (empfohlen: SSD 120 GB+)
  - Netzwerk: 1 GbE Netzwerkkarte
- **Empfohlen für Produktion:**
  - CPU: Multi-Core Prozessor (Intel Xeon/AMD EPYC)
  - RAM: 32 GB+ (abhängig von VMs)
  - Festplatte: 2x SSD im RAID1 für System, separate Disks für VM Storage
  - Netzwerk: 2x 1 GbE oder 10 GbE

#### 1.2 Netzwerkplanung
- **IP-Adressierung festlegen:**
  - Management-IP für Proxmox (z.B. 192.168.1.10/24)
  - Gateway-Adresse (z.B. 192.168.1.1)
  - DNS-Server (z.B. 8.8.8.8, 1.1.1.1)
  - VM-Netzwerk-Bereich (z.B. 192.168.1.100-200)

#### 1.3 Netzwerk-Diagramm erstellen
```
Internet
    |
[Router/Firewall] 192.168.1.1
    |
    |--- [Switch]
            |
            |--- [Proxmox Server] 192.168.1.10 (NIC1 - vmbr0)
            |--- [Optional: NIC2] 192.168.2.10 (Management)
            |--- [VMs] 192.168.1.100-200
```

#### 1.4 Download vorbereiten
- Proxmox VE ISO herunterladen: https://www.proxmox.com/de/downloads
- USB-Stick vorbereiten (min. 4 GB)
- Tool zum Erstellen eines bootfähigen USB (z.B. Rufus, Etcher)

#### 1.5 Backup-Strategie planen (optional)
- Backup-Speicherort festlegen (NAS, externes Storage)
- Backup-Zeitplan definieren
- Retention-Policy festlegen

---

## Milestone II: Hardware-Vorbereitung und Proxmox Installation

### Ziel
Proxmox VE auf der Hardware installieren.

### Schritt-für-Schritt Anleitung

#### 2.1 Bootfähigen USB-Stick erstellen
1. Proxmox VE ISO herunterladen
2. Rufus oder Etcher öffnen
3. USB-Stick auswählen
4. ISO-Datei auswählen
5. "Start" klicken und warten

#### 2.2 BIOS/UEFI Konfiguration
1. Server starten und ins BIOS/UEFI (meist F2, F10, DEL)
2. **Virtualisierung aktivieren:**
   - Intel: VT-x und VT-d aktivieren
   - AMD: AMD-V und AMD-Vi aktivieren
3. **Boot-Reihenfolge:**
   - USB als erste Boot-Option setzen
4. Einstellungen speichern und neustarten

#### 2.3 Proxmox Installation starten
1. Von USB-Stick booten
2. "Install Proxmox VE" auswählen
3. EULA akzeptieren
4. **Zielfestplatte auswählen:**
   - Festplatte für Installation wählen
   - Filesystem: ext4 (Standard) oder ZFS (für RAID)
   - Bei ZFS: RAID-Level wählen (RAID1, RAID10, etc.)

#### 2.4 Netzwerk und Hostname konfigurieren
1. **Hostname:** pve.lokaldomain.local (oder eigener FQDN)
2. **IP-Adresse:** 192.168.1.10/24 (geplante IP)
3. **Gateway:** 192.168.1.1
4. **DNS:** 8.8.8.8

#### 2.5 Administratorkonto einrichten
1. **Root-Passwort:** Sicheres Passwort setzen (min. 12 Zeichen)
2. **E-Mail:** Admin E-Mail-Adresse eingeben
3. Installation bestätigen

#### 2.6 Installation abschließen
1. Installation abwarten (5-10 Minuten)
2. USB-Stick entfernen
3. Server neustarten
4. Im Browser öffnen: `https://192.168.1.10:8006`
5. Mit root und gesetztem Passwort anmelden

---

## Milestone III: Grundkonfiguration

### Ziel
Proxmox grundlegend konfigurieren und Updates durchführen.

### Schritt-für-Schritt Anleitung

#### 3.1 Erste Anmeldung
1. Browser öffnen: `https://<proxmox-ip>:8006`
2. Sicherheitswarnung akzeptieren (Self-Signed Cert)
3. Anmelden mit root und Passwort
4. Subscription-Hinweis bestätigen (OK)

#### 3.2 Repository-Konfiguration (No-Subscription)
1. **Shell öffnen:** Datacenter → Node → Shell
2. **Enterprise Repository deaktivieren:**
```bash
# Backup erstellen
cp /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak

# Enterprise Repo auskommentieren
echo "# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise" > /etc/apt/sources.list.d/pve-enterprise.list
```

3. **No-Subscription Repository hinzufügen:**
```bash
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
```

4. **Ceph Repository deaktivieren (falls nicht benötigt):**
```bash
echo "# deb http://download.proxmox.com/debian/ceph-quincy bookworm no-subscription" > /etc/apt/sources.list.d/ceph.list
```

#### 3.3 System-Updates durchführen
```bash
# Paketlisten aktualisieren
apt update

# Verfügbare Updates anzeigen
apt list --upgradable

# System aktualisieren
apt dist-upgrade -y

# Neustart (falls Kernel aktualisiert wurde)
reboot
```

#### 3.4 Zeitzone und NTP konfigurieren
1. **GUI:** Datacenter → Options
2. **Timezone:** Europe/Zurich (oder entsprechend)
3. **Über Shell:**
```bash
# Zeitzone setzen
timedatectl set-timezone Europe/Zurich

# NTP-Status prüfen
timedatectl status

# Chrony (NTP) Status prüfen
systemctl status chrony
```

#### 3.5 Sprache anpassen (optional)
1. GUI: Datacenter → Options
2. Language: Deutsch (de)

---

## Milestone IV: Netzwerk-Konfiguration

### Ziel
Netzwerk-Bridges und VLANs konfigurieren.

### Schritt-für-Schritt Anleitung

#### 4.1 Bestehende Netzwerk-Konfiguration prüfen
1. **GUI:** Node → Network
2. Standard-Bridge `vmbr0` sollte sichtbar sein
3. Physisches Interface (z.B. `enp0s31f6`) ist mit `vmbr0` verbunden

#### 4.2 Linux Bridge verstehen
```
vmbr0 (Bridge)
  |
  |-- enp0s31f6 (Physical NIC)
  |-- tap100i0 (VM 100)
  |-- tap101i0 (VM 101)
```

#### 4.3 Zusätzliche Bridge erstellen (optional)
1. **GUI:** Node → Network → Create → Linux Bridge
2. **Name:** vmbr1
3. **IPv4/CIDR:** leer lassen (für internes Netzwerk)
4. **Ports:** leer (kein physisches NIC)
5. **Kommentar:** Internal Network
6. Apply Configuration

#### 4.4 VLAN-fähige Bridge konfigurieren (optional)
1. **GUI:** Node → Network → vmbr0 bearbeiten
2. **VLAN aware:** Aktivieren
3. Apply Configuration

**VMs können dann VLAN-Tags verwenden:**
- VM → Network Device → VLAN Tag: 10

#### 4.5 Bond/LACP konfigurieren (für Redundanz - optional)
```bash
# Über Shell
auto bond0
iface bond0 inet manual
    bond-slaves enp0s31f6 enp0s32f7
    bond-miimon 100
    bond-mode 802.3ad
    bond-xmit-hash-policy layer2+3

auto vmbr0
iface vmbr0 inet static
    address 192.168.1.10/24
    gateway 192.168.1.1
    bridge-ports bond0
    bridge-stp off
    bridge-fd 0
```

#### 4.6 Netzwerk-Konfiguration testen
```bash
# IP-Konfiguration prüfen
ip addr show

# Bridge-Status prüfen
brctl show

# Ping-Test
ping -c 4 8.8.8.8
ping -c 4 google.com
```

---

## Milestone V: Storage-Konfiguration

### Ziel
Storage-Pools einrichten und konfigurieren.

### Schritt-für-Schritt Anleitung

#### 5.1 Verfügbare Storage-Typen verstehen
- **local:** Verzeichnis auf dem Host (VM Disks, ISOs)
- **local-lvm:** LVM-Thin Pool (VM Disks)
- **Directory:** Beliebiges Verzeichnis
- **NFS:** Network File System
- **CIFS/SMB:** Windows-Shares
- **ZFS:** ZFS Pool
- **Ceph:** Distributed Storage

#### 5.2 Standard-Storage prüfen
1. **GUI:** Datacenter → Storage
2. **local:** /var/lib/vz (ISO Images, Container Templates)
3. **local-lvm:** LVM-Thin (VM Disks, Container Volumes)

#### 5.3 Zusätzliche Festplatte hinzufügen
1. **Festplatte identifizieren:**
```bash
lsblk
fdisk -l
```

2. **LVM erstellen (Beispiel):**
```bash
# Partition erstellen
fdisk /dev/sdb
# n (new), p (primary), 1, Enter, Enter, w (write)

# Physical Volume erstellen
pvcreate /dev/sdb1

# Volume Group erstellen
vgcreate vg-data /dev/sdb1

# Logical Volume erstellen (Thin Pool)
lvcreate -L 100G -T vg-data/data-pool

# In Proxmox einbinden (GUI oder CLI)
```

3. **GUI:** Datacenter → Storage → Add → LVM-Thin
   - ID: vm-storage
   - Volume Group: vg-data
   - Thin Pool: data-pool
   - Content: Disk image, Container

#### 5.4 NFS-Storage hinzufügen (optional)
1. **NFS-Server vorbereiten** (auf NAS/anderem Server)
2. **GUI:** Datacenter → Storage → Add → NFS
   - ID: nfs-backup
   - Server: 192.168.1.50
   - Export: /mnt/backups
   - Content: VZDump backup file

#### 5.5 Directory-Storage hinzufügen
1. **Verzeichnis erstellen:**
```bash
mkdir -p /mnt/iso-storage
chmod 755 /mnt/iso-storage
```

2. **GUI:** Datacenter → Storage → Add → Directory
   - ID: iso-storage
   - Directory: /mnt/iso-storage
   - Content: ISO image, Container template

#### 5.6 Storage-Performance testen
```bash
# Schreib-Performance testen
dd if=/dev/zero of=/var/lib/vz/testfile bs=1M count=1024 oflag=direct

# Lese-Performance testen
dd if=/var/lib/vz/testfile of=/dev/null bs=1M iflag=direct

# Aufräumen
rm /var/lib/vz/testfile
```

---

## Milestone VI: Erste VMs und Container

### Ziel
Erste virtuelle Maschinen und Container erstellen.

### Schritt-für-Schritt Anleitung

#### 6.1 ISO-Images hochladen
1. **GUI:** Storage (local) → ISO Images → Upload
2. ISO-Datei auswählen (z.B. Ubuntu Server, Debian, Windows)
3. Upload abwarten

**Oder über CLI:**
```bash
cd /var/lib/vz/template/iso
wget https://releases.ubuntu.com/22.04/ubuntu-22.04.3-live-server-amd64.iso
```

#### 6.2 Erste VM erstellen (Ubuntu Server)
1. **GUI:** Rechtsklick auf Node → Create VM
2. **General:**
   - VM ID: 100
   - Name: ubuntu-server-01
3. **OS:**
   - ISO Image: ubuntu-22.04.3-live-server-amd64.iso
   - Type: Linux
   - Version: 6.x - 2.6 Kernel
4. **System:**
   - SCSI Controller: VirtIO SCSI
   - Qemu Agent: ✓ (aktivieren)
5. **Disks:**
   - Storage: local-lvm
   - Disk size: 32 GB
   - Cache: Write back (für bessere Performance)
6. **CPU:**
   - Sockets: 1
   - Cores: 2
   - Type: host (beste Performance)
7. **Memory:**
   - RAM: 2048 MB
8. **Network:**
   - Bridge: vmbr0
   - Model: VirtIO (paravirtualized)
9. **Confirm:** Start after created (✓)

#### 6.3 VM Installation durchführen
1. VM startet automatisch
2. **Console öffnen:** VM 100 → Console
3. Ubuntu Installation durchführen
4. **Qemu Guest Agent installieren (nach OS-Installation):**
```bash
sudo apt update
sudo apt install qemu-guest-agent
sudo systemctl start qemu-guest-agent
sudo systemctl enable qemu-guest-agent
```

#### 6.4 LXC Container erstellen
1. **Container Template herunterladen:**
   - GUI: local → CT Templates
   - Templates auswählen (z.B. ubuntu-22.04-standard)

2. **Container erstellen:**
   - Rechtsklick auf Node → Create CT
   - **General:**
     - CT ID: 200
     - Hostname: webserver
     - Password: (setzen)
   - **Template:**
     - Template: ubuntu-22.04-standard
   - **Disks:**
     - Storage: local-lvm
     - Disk size: 8 GB
   - **CPU:**
     - Cores: 2
   - **Memory:**
     - RAM: 512 MB
     - Swap: 512 MB
   - **Network:**
     - Bridge: vmbr0
     - IPv4: DHCP oder Static
   - **DNS:**
     - DNS: 8.8.8.8

3. **Container starten:**
   - Container 200 → Start
   - Console → Login mit root

#### 6.5 VM/Container Management
```bash
# VMs/Container auflisten
qm list        # VMs
pct list       # Container

# VM/Container starten/stoppen
qm start 100
qm stop 100
qm shutdown 100

pct start 200
pct stop 200
pct shutdown 200

# Snapshots erstellen
qm snapshot 100 backup-before-update
pct snapshot 200 pre-config

# Snapshots wiederherstellen
qm rollback 100 backup-before-update
pct rollback 200 pre-config
```

#### 6.6 Cloud-Init (optional)
1. **Cloud-Init fähiges Image herunterladen:**
```bash
wget https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
```

2. **VM erstellen und Image importieren:**
```bash
qm create 9000 --name ubuntu-cloud-template --memory 2048 --net0 virtio,bridge=vmbr0
qm importdisk 9000 jammy-server-cloudimg-amd64.img local-lvm
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-0
qm set 9000 --ide2 local-lvm:cloudinit
qm set 9000 --boot c --bootdisk scsi0
qm set 9000 --serial0 socket --vga serial0
qm set 9000 --agent enabled=1
qm template 9000
```

3. **VM aus Template klonen:**
```bash
qm clone 9000 101 --name web-01 --full
qm set 101 --sshkey ~/.ssh/id_rsa.pub
qm set 101 --ipconfig0 ip=192.168.1.101/24,gw=192.168.1.1
qm start 101
```

---

## Milestone VII: Absicherung und Monitoring

### Ziel
Proxmox absichern und Monitoring einrichten.

### Schritt-für-Schritt Anleitung

#### 7.1 Firewall aktivieren
1. **Datacenter-Firewall:**
   - GUI: Datacenter → Firewall → Options
   - Firewall: Enable (✓)

2. **Standard-Regeln erstellen:**
   - GUI: Datacenter → Firewall → Add
   - **SSH erlauben:**
     - Direction: in
     - Action: ACCEPT
     - Protocol: tcp
     - Dest. port: 22
   - **Proxmox Web-Interface:**
     - Protocol: tcp
     - Dest. port: 8006
   - **Ping erlauben:**
     - Protocol: icmp

3. **Node-Firewall aktivieren:**
   - GUI: Node → Firewall → Options
   - Firewall: Enable (✓)

#### 7.2 SSH absichern
```bash
# SSH-Konfiguration bearbeiten
nano /etc/ssh/sshd_config

# Änderungen:
PermitRootLogin prohibit-password  # Nur Key-Auth für root
PasswordAuthentication no          # Passwort-Auth deaktivieren
Port 22                             # Oder Custom Port

# SSH neustarten
systemctl restart sshd
```

#### 7.3 2FA einrichten
1. **GUI:** Datacenter → Permissions → Two Factor
2. **TOTP hinzufügen:**
   - User: root@pam
   - Description: Proxmox 2FA
   - QR-Code scannen mit Authenticator App

#### 7.4 Benutzer und Rollen
1. **Bereich erstellen:**
   - GUI: Datacenter → Permissions → Realms
   - Linux PAM (Standard) oder LDAP/AD

2. **Benutzer erstellen:**
   - Datacenter → Permissions → Users → Add
   - User: admin
   - Realm: pam
   - Password: (setzen)

3. **Rollen zuweisen:**
   - Datacenter → Permissions → Add → User Permission
   - Path: /
   - User: admin@pam
   - Role: PVEAdmin

#### 7.5 E-Mail-Benachrichtigungen
```bash
# Postfix installieren (falls nicht vorhanden)
apt install postfix mailutils

# Postfix konfigurieren für Relay
nano /etc/postfix/main.cf

# Beispiel für Gmail:
relayhost = [smtp.gmail.com]:587
smtp_use_tls = yes
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous

# Credentials speichern
echo "[smtp.gmail.com]:587 username@gmail.com:password" > /etc/postfix/sasl_passwd
postmap /etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd*

# Postfix neustarten
systemctl restart postfix

# Test-Mail senden
echo "Proxmox Test" | mail -s "Test Mail" admin@example.com
```

#### 7.6 Monitoring einrichten

**GUI-Monitoring:**
1. **GUI:** Node → Summary
   - CPU, RAM, Netzwerk, Storage in Echtzeit

**Erweiterte Monitoring-Tools (optional):**

```bash
# Prometheus Node Exporter installieren
apt install prometheus-node-exporter

# Grafana für Visualisierung (auf separater VM empfohlen)
```

#### 7.7 Log-Management
```bash
# System-Logs ansehen
journalctl -f                    # Live-Logs
journalctl -u pveproxy          # Proxmox Web-Interface
journalctl -u pvedaemon         # Proxmox Daemon
journalctl -u pve-cluster       # Cluster

# Log-Dateien
tail -f /var/log/syslog
tail -f /var/log/pve/tasks/active
```

#### 7.8 Automatische Updates (optional, mit Vorsicht)
```bash
# Unattended-Upgrades installieren
apt install unattended-upgrades

# Konfigurieren
dpkg-reconfigure -plow unattended-upgrades

# /etc/apt/apt.conf.d/50unattended-upgrades bearbeiten
nano /etc/apt/apt.conf.d/50unattended-upgrades

# Nur Security-Updates aktivieren
Unattended-Upgrade::Origins-Pattern {
    "origin=Debian,codename=${distro_codename},label=Debian-Security";
};
```

#### 7.9 Ressourcen-Limits setzen
```bash
# Für VMs: GUI → VM → Options → Resource Limits
# Für Container: GUI → CT → Options → CPU Limit, Memory Limit

# Oder via CLI:
qm set 100 --cpulimit 2       # Max 2 CPUs
qm set 100 --cpuunits 1024    # CPU-Priorität

pct set 200 --cpulimit 1
pct set 200 --memory 512
```

---

## Optional: Backup-Konfiguration

### Ziel
Automatische Backups für VMs und Container einrichten.

### Schritt-für-Schritt Anleitung

#### O.1 Backup-Storage vorbereiten
1. **NFS/CIFS-Share** einrichten (siehe Milestone V)
2. **Oder lokales Backup-Verzeichnis:**
```bash
mkdir -p /backup
```

3. **GUI:** Datacenter → Storage → Add → Directory
   - ID: backup
   - Directory: /backup
   - Content: VZDump backup file

#### O.2 Backup-Job erstellen
1. **GUI:** Datacenter → Backup → Add
2. **Konfiguration:**
   - Node: (Node auswählen)
   - Storage: backup (oder nfs-backup)
   - Schedule: Daily, 02:00
   - Selection Mode: All
   - Compression: ZSTD (beste Kompression)
   - Mode: Snapshot (für laufende VMs)
   - Enable: ✓

3. **Retention-Policy:**
   - Keep last: 7 (7 Tage)
   - Keep daily: 4 (4 Wochen)
   - Keep weekly: 4 (4 Wochen)
   - Keep monthly: 3 (3 Monate)

#### O.3 Manuelles Backup erstellen
1. **GUI:** VM/CT auswählen → Backup → Backup now
2. **Oder via CLI:**
```bash
# VM Backup
vzdump 100 --storage backup --mode snapshot --compress zstd

# Container Backup
vzdump 200 --storage backup --mode snapshot --compress zstd

# Alle VMs/Container
vzdump --all --storage backup --mode snapshot
```

#### O.4 Backup wiederherstellen
1. **GUI:** Node → Backup → Backup-Datei auswählen → Restore
2. **Konfiguration:**
   - VM ID: 100 (Original) oder neue ID
   - Storage: local-lvm
   - Start after restore: ✓ (optional)

3. **Oder via CLI:**
```bash
qmrestore /backup/vzdump-qemu-100-2024_01_15-02_00_00.vma.zst 100
```

#### O.5 Backup-Verifizierung
```bash
# Backup-Logs prüfen
cat /var/log/pve/tasks/active

# Backup-Dateien auflisten
ls -lh /backup/

# Backup-Größe prüfen
du -sh /backup/*
```

#### O.6 Externe Backup-Synchronisation
```bash
# Rsync zu externem Server
rsync -avz --progress /backup/ backup-server:/proxmox-backups/

# Oder mit Cron-Job automatisieren
crontab -e

# Täglich um 04:00 synchronisieren
0 4 * * * rsync -avz /backup/ backup-server:/proxmox-backups/ >> /var/log/backup-sync.log 2>&1
```

#### O.7 Proxmox Backup Server (PBS) Integration (optional)
1. **PBS installieren** (auf separatem Server/VM)
2. **GUI:** Datacenter → Storage → Add → Proxmox Backup Server
   - ID: pbs
   - Server: pbs.example.com
   - Username: backup@pbs
   - Password: (PBS-Passwort)
   - Datastore: proxmox-backups

3. **Backup-Job auf PBS umstellen:**
   - Datacenter → Backup → Job bearbeiten
   - Storage: pbs

---

## Optional: NIC2 für Management

### Ziel
Separates Management-Netzwerk über zweite Netzwerkkarte einrichten.

### Schritt-für-Schritt Anleitung

#### M.1 Hardware-Voraussetzungen
- Zweite physische Netzwerkkarte im Server
- Separater Switch/VLAN für Management
- Getrenntes IP-Subnetz (z.B. 192.168.2.0/24)

#### M.2 Zweite Netzwerkkarte identifizieren
```bash
# Alle Netzwerk-Interfaces auflisten
ip link show

# Beispiel-Output:
# 1: lo: ...
# 2: enp0s31f6: ...  (NIC1 - Produktion)
# 3: enp0s32f7: ...  (NIC2 - Management)
```

#### M.3 Management-Bridge erstellen
1. **GUI:** Node → Network → Create → Linux Bridge
2. **Konfiguration:**
   - Name: vmbr1
   - IPv4/CIDR: 192.168.2.10/24
   - Gateway: (leer lassen, kein Default-Gateway)
   - Bridge ports: enp0s32f7 (zweite NIC)
   - Autostart: ✓
   - VLAN aware: ✗
   - Comment: Management Network

3. **Apply Configuration**

#### M.4 Firewall-Regeln für Management
1. **GUI:** Datacenter → Firewall → Security Group → Add
2. **Security Group erstellen:**
   - Name: management-access
   - **Regeln:**
     - SSH (22): nur von Management-Netz
     - Proxmox Web (8006): nur von Management-Netz
     - ICMP: allow

3. **Regel-Beispiele:**
```bash
# SSH nur von Management-Netz
Direction: in
Action: ACCEPT
Protocol: tcp
Source: 192.168.2.0/24
Dest. port: 22

# Proxmox Web Interface
Direction: in
Action: ACCEPT
Protocol: tcp
Source: 192.168.2.0/24
Dest. port: 8006

# Alles andere blockieren (auf vmbr0)
Direction: in
Action: DROP
Protocol: tcp
Dest. port: 22,8006
Interface: vmbr0
```

#### M.5 Management-Zugriff testen
```bash
# Von Management-Netzwerk (192.168.2.0/24):
ssh root@192.168.2.10
# Browser: https://192.168.2.10:8006

# Von Produktions-Netzwerk sollte blockiert sein
ssh root@192.168.1.10  # → Timeout/Rejected
```

#### M.6 Netzwerk-Routing konfigurieren
```bash
# Sicherstellen, dass beide Netze nicht routen (Sicherheit)
nano /etc/sysctl.conf

# Diese Zeile sollte auf 0 stehen:
net.ipv4.ip_forward=0

# Änderungen anwenden
sysctl -p
```

#### M.7 IPMI/iLO über Management-Netz (Hardware-abhängig)
Falls Server IPMI/iLO/iDRAC hat:
1. **IPMI auf Management-VLAN setzen:**
   - IP: 192.168.2.11
   - Gateway: 192.168.2.1 (Management-Router)
2. **Zugriff nur über Management-Netz:**
   - Browser: https://192.168.2.11
   - Voller Hardware-Zugriff (KVM, Power, etc.)

#### M.8 Dokumentation der Netzwerk-Architektur
```
[Internet]
    |
[Router] 192.168.1.1
    |
    |--- [Production VLAN - VLAN10] 192.168.1.0/24
    |        |
    |        |--- vmbr0 (enp0s31f6) - 192.168.1.10
    |        |--- VMs/Container - 192.168.1.100-200
    |
    |--- [Management VLAN - VLAN20] 192.168.2.0/24
             |
             |--- vmbr1 (enp0s32f7) - 192.168.2.10
             |--- IPMI - 192.168.2.11
             |--- Admin-PC - 192.168.2.50
```

---

## Anhang

### Nützliche Befehle

#### System
```bash
# Proxmox Version
pveversion -v

# System-Ressourcen
pvesh get /nodes/localhost/status

# Cluster-Status (falls Cluster)
pvecm status
```

#### VM/Container
```bash
# VM-Konfiguration anzeigen
qm config 100

# Container-Konfiguration
pct config 200

# VM migrieren (bei Cluster)
qm migrate 100 node2

# VM klonen
qm clone 100 101 --name clone-vm
```

#### Storage
```bash
# Storage-Status
pvesm status

# LVM-Status
lvs
vgs
pvs
```

#### Netzwerk
```bash
# Bridge-Status
brctl show

# Netzwerk-Performance
iperf3 -s  # Server
iperf3 -c <server-ip>  # Client
```

### Troubleshooting

#### Proxmox Web-Interface nicht erreichbar
```bash
# Service-Status prüfen
systemctl status pveproxy
systemctl status pvedaemon

# Neustart
systemctl restart pveproxy
systemctl restart pvedaemon

# Logs prüfen
journalctl -u pveproxy -f
```

#### VM startet nicht
```bash
# Status prüfen
qm status 100

# Logs ansehen
qm showcmd 100

# Konfiguration prüfen
qm config 100

# Im Zweifelsfall: Snapshot zurückrollen
```

#### Netzwerk-Probleme
```bash
# Bridge neu starten
ifreload -a

# Netzwerk-Service neustarten
systemctl restart networking

# Konfiguration prüfen
cat /etc/network/interfaces
```

### Best Practices

1. **Regelmäßige Backups:** Mindestens täglich, 3-2-1 Regel
2. **Updates:** Monatlich, nach Test auf Test-System
3. **Monitoring:** Ressourcen-Nutzung überwachen
4. **Dokumentation:** Alle Änderungen dokumentieren
5. **Snapshots:** Vor jeder Änderung Snapshot erstellen
6. **Sicherheit:** Firewall, 2FA, SSH-Keys, getrennte Netze
7. **Ressourcen-Limits:** Für alle VMs/Container setzen
8. **High Availability:** Bei kritischen Systemen Cluster verwenden

### Weiterführende Ressourcen

- **Offizielle Dokumentation:** https://pve.proxmox.com/pve-docs/
- **Proxmox Forum:** https://forum.proxmox.com/
- **Proxmox Wiki:** https://pve.proxmox.com/wiki/
- **YouTube Kanäle:**
  - Learn Linux TV
  - Techno Tim
  - Craft Computing

---

**Version:** 1.0
**Erstellt:** Mai 2026
**Autor:** Proxmox Installations-Guide
