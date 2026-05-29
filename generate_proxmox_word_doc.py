#!/usr/bin/env python3
"""
Generate a professional Word document for the Proxmox Server installation guide
with formatting, styling, and network diagrams.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io
from PIL import Image, ImageDraw, ImageFont

def create_network_diagram():
    """Create a simple network diagram using PIL"""
    # Create image
    width, height = 800, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Colors
    blue = (52, 152, 219)
    green = (46, 204, 113)
    orange = (230, 126, 34)
    gray = (149, 165, 166)

    # Draw Internet cloud
    draw.ellipse([300, 20, 500, 100], outline=blue, width=3)
    draw.text((370, 50), "Internet", fill=blue, font=font)

    # Draw Router
    draw.rectangle([320, 140, 480, 200], outline=green, fill=(46, 204, 113, 50), width=2)
    draw.text((330, 155), "Router/Firewall", fill=(0, 0, 0), font=font)
    draw.text((340, 175), "192.168.1.1", fill=(0, 0, 0), font=font_small)

    # Connection from Internet to Router
    draw.line([400, 100, 400, 140], fill=gray, width=2)

    # Draw Switch
    draw.rectangle([320, 260, 480, 320], outline=orange, fill=(230, 126, 34, 50), width=2)
    draw.text((360, 280), "Switch", fill=(0, 0, 0), font=font)

    # Connection from Router to Switch
    draw.line([400, 200, 400, 260], fill=gray, width=2)

    # Draw Proxmox Server
    draw.rectangle([280, 380, 520, 460], outline=(192, 57, 43), fill=(192, 57, 43, 50), width=3)
    draw.text((310, 395), "Proxmox Server", fill=(0, 0, 0), font=font)
    draw.text((310, 415), "192.168.1.10", fill=(0, 0, 0), font=font_small)
    draw.text((310, 435), "NIC1 - vmbr0", fill=(0, 0, 0), font=font_small)

    # Connection from Switch to Proxmox
    draw.line([400, 320, 400, 380], fill=gray, width=2)

    # Draw VMs
    vm_y = 380
    draw.rectangle([60, vm_y, 220, vm_y+60], outline=blue, fill=(52, 152, 219, 50), width=2)
    draw.text((80, vm_y+15), "VMs/Container", fill=(0, 0, 0), font=font)
    draw.text((70, vm_y+35), "192.168.1.100-200", fill=(0, 0, 0), font=font_small)

    # Connection from Switch to VMs
    draw.line([320, 290, 220, 290], fill=gray, width=2)
    draw.line([220, 290, 220, vm_y], fill=gray, width=2)

    # Draw optional Management NIC
    draw.rectangle([560, 380, 740, 460], outline=(155, 89, 182), fill=(155, 89, 182, 50), width=2)
    draw.text((570, 395), "Management", fill=(0, 0, 0), font=font)
    draw.text((570, 415), "192.168.2.10", fill=(0, 0, 0), font=font_small)
    draw.text((570, 435), "NIC2 (Optional)", fill=(0, 0, 0), font=font_small)

    # Dotted line for optional connection
    for i in range(480, 560, 10):
        draw.line([i, 420, i+5, 420], fill=gray, width=2)

    # Save to BytesIO
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_bridge_diagram():
    """Create a Linux Bridge diagram"""
    width, height = 600, 400
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Colors
    blue = (52, 152, 219)
    green = (46, 204, 113)

    # Draw vmbr0 (Bridge)
    draw.rectangle([200, 50, 400, 120], outline=blue, fill=(52, 152, 219, 50), width=3)
    draw.text((250, 75), "vmbr0 (Bridge)", fill=(0, 0, 0), font=font)

    # Draw Physical NIC
    draw.rectangle([200, 200, 400, 270], outline=green, fill=(46, 204, 113, 50), width=2)
    draw.text((230, 225), "enp0s31f6", fill=(0, 0, 0), font=font)
    draw.text((240, 245), "(Physical NIC)", fill=(0, 0, 0), font=font_small)

    # Connection
    draw.line([300, 120, 300, 200], fill=(0, 0, 0), width=2)

    # Draw VMs
    vm1_x, vm2_x = 50, 450
    for i, (x, vm_id) in enumerate([(vm1_x, "100"), (vm2_x, "101")]):
        draw.rectangle([x, 200, x+120, 270], outline=(192, 57, 43), fill=(192, 57, 43, 50), width=2)
        draw.text((x+10, 225), f"VM {vm_id}", fill=(0, 0, 0), font=font)
        draw.text((x+10, 245), f"tap{vm_id}i0", fill=(0, 0, 0), font=font_small)

        # Connection to bridge
        if i == 0:
            draw.line([x+60, 200, 200, 85], fill=(0, 0, 0), width=2)
        else:
            draw.line([x+60, 200, 400, 85], fill=(0, 0, 0), width=2)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone_icon(number, color):
    """Create a milestone icon"""
    size = 100
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Draw circle
    draw.ellipse([10, 10, 90, 90], outline=color, fill=color, width=3)

    # Draw number
    text = str(number)
    # Center the text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 5
    draw.text((x, y), text, fill='white', font=font)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def add_hyperlink(paragraph, text, url):
    """Add a hyperlink to a paragraph"""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Style as hyperlink
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0563C1')
    rPr.append(color)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)
    return hyperlink

def create_word_document():
    """Create the complete Word document"""
    doc = Document()

    # Set document margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title Page
    title = doc.add_heading('Proxmox Server', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.color.rgb = RGBColor(192, 57, 43)
    title.runs[0].font.size = Pt(36)

    subtitle = doc.add_paragraph('Komplette Installations- und Konfigurationsanleitung')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(18)
    subtitle.runs[0].font.color.rgb = RGBColor(52, 73, 94)

    doc.add_paragraph()
    doc.add_paragraph()

    # Add network diagram on title page
    network_img = create_network_diagram()
    doc.add_picture(network_img, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Version info
    version = doc.add_paragraph()
    version.alignment = WD_ALIGN_PARAGRAPH.CENTER
    version.add_run('Version 1.0 | Mai 2026').font.size = Pt(11)

    doc.add_page_break()

    # Table of Contents
    toc_heading = doc.add_heading('Inhaltsverzeichnis', 1)
    toc_heading.runs[0].font.color.rgb = RGBColor(41, 128, 185)

    toc_items = [
        'Milestone I: Vorbereitung und Planung',
        'Milestone II: Hardware-Vorbereitung und Proxmox Installation',
        'Milestone III: Grundkonfiguration',
        'Milestone IV: Netzwerk-Konfiguration',
        'Milestone V: Storage-Konfiguration',
        'Milestone VI: Erste VMs und Container',
        'Milestone VII: Absicherung und Monitoring',
        'Optional: Backup-Konfiguration',
        'Optional: NIC2 für Management',
        'Anhang: Nützliche Befehle',
        'Troubleshooting',
        'Best Practices'
    ]

    for item in toc_items:
        p = doc.add_paragraph(item, style='List Bullet')
        p.runs[0].font.size = Pt(12)

    doc.add_page_break()

    # Milestone colors
    milestone_colors = [
        (231, 76, 60),   # Red
        (230, 126, 34),  # Orange
        (241, 196, 15),  # Yellow
        (46, 204, 113),  # Green
        (52, 152, 219),  # Blue
        (155, 89, 182),  # Purple
        (52, 73, 94),    # Dark Blue
    ]

    # Milestone I
    doc.add_heading('Milestone I: Vorbereitung und Planung', 1)

    # Add milestone icon
    icon1 = create_milestone_icon(1, milestone_colors[0])
    doc.add_picture(icon1, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Hardware-Anforderungen klären und Netzwerkplanung durchführen.')

    doc.add_heading('1.1 Hardware-Anforderungen prüfen', 3)

    p = doc.add_paragraph()
    p.add_run('Minimum:').bold = True
    doc.add_paragraph('CPU: 64-bit Prozessor mit Intel VT/AMD-V Support', style='List Bullet')
    doc.add_paragraph('RAM: 4 GB (empfohlen: 8 GB+)', style='List Bullet')
    doc.add_paragraph('Festplatte: 32 GB (empfohlen: SSD 120 GB+)', style='List Bullet')
    doc.add_paragraph('Netzwerk: 1 GbE Netzwerkkarte', style='List Bullet')

    p = doc.add_paragraph()
    p.add_run('Empfohlen für Produktion:').bold = True
    doc.add_paragraph('CPU: Multi-Core Prozessor (Intel Xeon/AMD EPYC)', style='List Bullet')
    doc.add_paragraph('RAM: 32 GB+ (abhängig von VMs)', style='List Bullet')
    doc.add_paragraph('Festplatte: 2x SSD im RAID1 für System, separate Disks für VM Storage', style='List Bullet')
    doc.add_paragraph('Netzwerk: 2x 1 GbE oder 10 GbE', style='List Bullet')

    doc.add_heading('1.2 Netzwerkplanung', 3)
    p = doc.add_paragraph()
    p.add_run('IP-Adressierung festlegen:').bold = True
    doc.add_paragraph('Management-IP für Proxmox (z.B. 192.168.1.10/24)', style='List Bullet')
    doc.add_paragraph('Gateway-Adresse (z.B. 192.168.1.1)', style='List Bullet')
    doc.add_paragraph('DNS-Server (z.B. 8.8.8.8, 1.1.1.1)', style='List Bullet')
    doc.add_paragraph('VM-Netzwerk-Bereich (z.B. 192.168.1.100-200)', style='List Bullet')

    doc.add_heading('1.3 Netzwerk-Diagramm', 3)
    network_img = create_network_diagram()
    doc.add_picture(network_img, width=Inches(5.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('1.4 Download vorbereiten', 3)
    doc.add_paragraph('Proxmox VE ISO herunterladen:', style='List Bullet')
    p = doc.add_paragraph('    ', style='List Bullet')
    add_hyperlink(p, 'https://www.proxmox.com/de/downloads', 'https://www.proxmox.com/de/downloads')
    doc.add_paragraph('USB-Stick vorbereiten (min. 4 GB)', style='List Bullet')
    doc.add_paragraph('Tool zum Erstellen eines bootfähigen USB (z.B. Rufus, Etcher)', style='List Bullet')

    doc.add_page_break()

    # Milestone II
    doc.add_heading('Milestone II: Hardware-Vorbereitung und Proxmox Installation', 1)
    icon2 = create_milestone_icon(2, milestone_colors[1])
    doc.add_picture(icon2, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Proxmox VE auf der Hardware installieren.')

    doc.add_heading('2.1 Bootfähigen USB-Stick erstellen', 3)
    doc.add_paragraph('1. Proxmox VE ISO herunterladen', style='List Number')
    doc.add_paragraph('2. Rufus oder Etcher öffnen', style='List Number')
    doc.add_paragraph('3. USB-Stick auswählen', style='List Number')
    doc.add_paragraph('4. ISO-Datei auswählen', style='List Number')
    doc.add_paragraph('5. "Start" klicken und warten', style='List Number')

    doc.add_heading('2.2 BIOS/UEFI Konfiguration', 3)
    doc.add_paragraph('1. Server starten und ins BIOS/UEFI (meist F2, F10, DEL)', style='List Number')
    p = doc.add_paragraph('2. ', style='List Number')
    p.add_run('Virtualisierung aktivieren:').bold = True
    doc.add_paragraph('Intel: VT-x und VT-d aktivieren', style='List Bullet 2')
    doc.add_paragraph('AMD: AMD-V und AMD-Vi aktivieren', style='List Bullet 2')
    p = doc.add_paragraph('3. ', style='List Number')
    p.add_run('Boot-Reihenfolge:').bold = True
    doc.add_paragraph('USB als erste Boot-Option setzen', style='List Bullet 2')
    doc.add_paragraph('4. Einstellungen speichern und neustarten', style='List Number')

    doc.add_heading('2.3 Proxmox Installation starten', 3)
    doc.add_paragraph('1. Von USB-Stick booten', style='List Number')
    doc.add_paragraph('2. "Install Proxmox VE" auswählen', style='List Number')
    doc.add_paragraph('3. EULA akzeptieren', style='List Number')
    p = doc.add_paragraph('4. ', style='List Number')
    p.add_run('Zielfestplatte auswählen:').bold = True
    doc.add_paragraph('Festplatte für Installation wählen', style='List Bullet 2')
    doc.add_paragraph('Filesystem: ext4 (Standard) oder ZFS (für RAID)', style='List Bullet 2')
    doc.add_paragraph('Bei ZFS: RAID-Level wählen (RAID1, RAID10, etc.)', style='List Bullet 2')

    doc.add_heading('2.4 Netzwerk und Hostname konfigurieren', 3)
    doc.add_paragraph('Hostname: pve.lokaldomain.local (oder eigener FQDN)', style='List Bullet')
    doc.add_paragraph('IP-Adresse: 192.168.1.10/24 (geplante IP)', style='List Bullet')
    doc.add_paragraph('Gateway: 192.168.1.1', style='List Bullet')
    doc.add_paragraph('DNS: 8.8.8.8', style='List Bullet')

    doc.add_heading('2.5 Administratorkonto einrichten', 3)
    doc.add_paragraph('Root-Passwort: Sicheres Passwort setzen (min. 12 Zeichen)', style='List Bullet')
    doc.add_paragraph('E-Mail: Admin E-Mail-Adresse eingeben', style='List Bullet')
    doc.add_paragraph('Installation bestätigen', style='List Bullet')

    doc.add_page_break()

    # Milestone III
    doc.add_heading('Milestone III: Grundkonfiguration', 1)
    icon3 = create_milestone_icon(3, milestone_colors[2])
    doc.add_picture(icon3, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Proxmox grundlegend konfigurieren und Updates durchführen.')

    doc.add_heading('3.1 Erste Anmeldung', 3)
    doc.add_paragraph('1. Browser öffnen: https://<proxmox-ip>:8006', style='List Number')
    doc.add_paragraph('2. Sicherheitswarnung akzeptieren (Self-Signed Cert)', style='List Number')
    doc.add_paragraph('3. Anmelden mit root und Passwort', style='List Number')
    doc.add_paragraph('4. Subscription-Hinweis bestätigen (OK)', style='List Number')

    doc.add_heading('3.2 Repository-Konfiguration (No-Subscription)', 3)
    doc.add_paragraph('Shell öffnen: Datacenter → Node → Shell')

    p = doc.add_paragraph()
    p.add_run('Enterprise Repository deaktivieren:').bold = True
    code = doc.add_paragraph(
        'cp /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/pve-enterprise.list.bak\n'
        'echo "# deb https://enterprise.proxmox.com/debian/pve bookworm pve-enterprise" > /etc/apt/sources.list.d/pve-enterprise.list',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    p = doc.add_paragraph()
    p.add_run('No-Subscription Repository hinzufügen:').bold = True
    code = doc.add_paragraph(
        'echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('3.3 System-Updates durchführen', 3)
    code = doc.add_paragraph(
        'apt update\n'
        'apt list --upgradable\n'
        'apt dist-upgrade -y\n'
        'reboot',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # Milestone IV
    doc.add_heading('Milestone IV: Netzwerk-Konfiguration', 1)
    icon4 = create_milestone_icon(4, milestone_colors[3])
    doc.add_picture(icon4, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Netzwerk-Bridges und VLANs konfigurieren.')

    doc.add_heading('4.1 Bestehende Netzwerk-Konfiguration prüfen', 3)
    doc.add_paragraph('GUI: Node → Network', style='List Bullet')
    doc.add_paragraph('Standard-Bridge vmbr0 sollte sichtbar sein', style='List Bullet')
    doc.add_paragraph('Physisches Interface (z.B. enp0s31f6) ist mit vmbr0 verbunden', style='List Bullet')

    doc.add_heading('4.2 Linux Bridge verstehen', 3)
    bridge_img = create_bridge_diagram()
    doc.add_picture(bridge_img, width=Inches(4.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('4.3 Zusätzliche Bridge erstellen (optional)', 3)
    doc.add_paragraph('1. GUI: Node → Network → Create → Linux Bridge', style='List Number')
    doc.add_paragraph('2. Name: vmbr1', style='List Number')
    doc.add_paragraph('3. IPv4/CIDR: leer lassen (für internes Netzwerk)', style='List Number')
    doc.add_paragraph('4. Ports: leer (kein physisches NIC)', style='List Number')
    doc.add_paragraph('5. Kommentar: Internal Network', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')

    doc.add_page_break()

    # Milestone V
    doc.add_heading('Milestone V: Storage-Konfiguration', 1)
    icon5 = create_milestone_icon(5, milestone_colors[4])
    doc.add_picture(icon5, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Storage-Pools einrichten und konfigurieren.')

    doc.add_heading('5.1 Verfügbare Storage-Typen verstehen', 3)
    doc.add_paragraph('local: Verzeichnis auf dem Host (VM Disks, ISOs)', style='List Bullet')
    doc.add_paragraph('local-lvm: LVM-Thin Pool (VM Disks)', style='List Bullet')
    doc.add_paragraph('Directory: Beliebiges Verzeichnis', style='List Bullet')
    doc.add_paragraph('NFS: Network File System', style='List Bullet')
    doc.add_paragraph('CIFS/SMB: Windows-Shares', style='List Bullet')
    doc.add_paragraph('ZFS: ZFS Pool', style='List Bullet')
    doc.add_paragraph('Ceph: Distributed Storage', style='List Bullet')

    doc.add_heading('5.2 Standard-Storage prüfen', 3)
    doc.add_paragraph('GUI: Datacenter → Storage', style='List Bullet')
    doc.add_paragraph('local: /var/lib/vz (ISO Images, Container Templates)', style='List Bullet')
    doc.add_paragraph('local-lvm: LVM-Thin (VM Disks, Container Volumes)', style='List Bullet')

    doc.add_page_break()

    # Milestone VI
    doc.add_heading('Milestone VI: Erste VMs und Container', 1)
    icon6 = create_milestone_icon(6, milestone_colors[5])
    doc.add_picture(icon6, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Erste virtuelle Maschinen und Container erstellen.')

    doc.add_heading('6.1 ISO-Images hochladen', 3)
    doc.add_paragraph('1. GUI: Storage (local) → ISO Images → Upload', style='List Number')
    doc.add_paragraph('2. ISO-Datei auswählen (z.B. Ubuntu Server, Debian, Windows)', style='List Number')
    doc.add_paragraph('3. Upload abwarten', style='List Number')

    doc.add_heading('6.2 Erste VM erstellen (Ubuntu Server)', 3)
    doc.add_paragraph('1. GUI: Rechtsklick auf Node → Create VM', style='List Number')

    p = doc.add_paragraph('2. ', style='List Number')
    p.add_run('General:').bold = True
    doc.add_paragraph('VM ID: 100', style='List Bullet 2')
    doc.add_paragraph('Name: ubuntu-server-01', style='List Bullet 2')

    p = doc.add_paragraph('3. ', style='List Number')
    p.add_run('OS:').bold = True
    doc.add_paragraph('ISO Image: ubuntu-22.04.3-live-server-amd64.iso', style='List Bullet 2')
    doc.add_paragraph('Type: Linux', style='List Bullet 2')

    p = doc.add_paragraph('4. ', style='List Number')
    p.add_run('System:').bold = True
    doc.add_paragraph('SCSI Controller: VirtIO SCSI', style='List Bullet 2')
    doc.add_paragraph('Qemu Agent: ✓ (aktivieren)', style='List Bullet 2')

    p = doc.add_paragraph('5. ', style='List Number')
    p.add_run('Disks:').bold = True
    doc.add_paragraph('Storage: local-lvm', style='List Bullet 2')
    doc.add_paragraph('Disk size: 32 GB', style='List Bullet 2')

    p = doc.add_paragraph('6. ', style='List Number')
    p.add_run('CPU:').bold = True
    doc.add_paragraph('Sockets: 1, Cores: 2', style='List Bullet 2')

    p = doc.add_paragraph('7. ', style='List Number')
    p.add_run('Memory:').bold = True
    doc.add_paragraph('RAM: 2048 MB', style='List Bullet 2')

    p = doc.add_paragraph('8. ', style='List Number')
    p.add_run('Network:').bold = True
    doc.add_paragraph('Bridge: vmbr0', style='List Bullet 2')
    doc.add_paragraph('Model: VirtIO (paravirtualized)', style='List Bullet 2')

    doc.add_page_break()

    # Milestone VII
    doc.add_heading('Milestone VII: Absicherung und Monitoring', 1)
    icon7 = create_milestone_icon(7, milestone_colors[6])
    doc.add_picture(icon7, width=Inches(0.7))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Proxmox absichern und Monitoring einrichten.')

    doc.add_heading('7.1 Firewall aktivieren', 3)
    p = doc.add_paragraph()
    p.add_run('Datacenter-Firewall:').bold = True
    doc.add_paragraph('GUI: Datacenter → Firewall → Options', style='List Bullet')
    doc.add_paragraph('Firewall: Enable (✓)', style='List Bullet')

    p = doc.add_paragraph()
    p.add_run('Standard-Regeln erstellen:').bold = True
    doc.add_paragraph('SSH erlauben: Port 22', style='List Bullet')
    doc.add_paragraph('Proxmox Web-Interface: Port 8006', style='List Bullet')
    doc.add_paragraph('Ping erlauben: ICMP', style='List Bullet')

    doc.add_heading('7.2 SSH absichern', 3)
    code = doc.add_paragraph(
        'nano /etc/ssh/sshd_config\n\n'
        'PermitRootLogin prohibit-password\n'
        'PasswordAuthentication no\n\n'
        'systemctl restart sshd',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('7.3 2FA einrichten', 3)
    doc.add_paragraph('1. GUI: Datacenter → Permissions → Two Factor', style='List Number')
    doc.add_paragraph('2. TOTP hinzufügen: User: root@pam', style='List Number')
    doc.add_paragraph('3. QR-Code scannen mit Authenticator App', style='List Number')

    doc.add_page_break()

    # Optional: Backup
    doc.add_heading('Optional: Backup-Konfiguration', 1)

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Automatische Backups für VMs und Container einrichten.')

    doc.add_heading('O.1 Backup-Storage vorbereiten', 3)
    doc.add_paragraph('1. NFS/CIFS-Share einrichten (siehe Milestone V)', style='List Number')
    doc.add_paragraph('2. Oder lokales Backup-Verzeichnis: mkdir -p /backup', style='List Number')
    doc.add_paragraph('3. GUI: Datacenter → Storage → Add → Directory', style='List Number')

    doc.add_heading('O.2 Backup-Job erstellen', 3)
    doc.add_paragraph('1. GUI: Datacenter → Backup → Add', style='List Number')
    doc.add_paragraph('2. Storage: backup (oder nfs-backup)', style='List Number')
    doc.add_paragraph('3. Schedule: Daily, 02:00', style='List Number')
    doc.add_paragraph('4. Compression: ZSTD', style='List Number')
    doc.add_paragraph('5. Mode: Snapshot (für laufende VMs)', style='List Number')

    p = doc.add_paragraph()
    p.add_run('Retention-Policy:').bold = True
    doc.add_paragraph('Keep last: 7 (7 Tage)', style='List Bullet')
    doc.add_paragraph('Keep daily: 4 (4 Wochen)', style='List Bullet')
    doc.add_paragraph('Keep weekly: 4 (4 Wochen)', style='List Bullet')
    doc.add_paragraph('Keep monthly: 3 (3 Monate)', style='List Bullet')

    doc.add_page_break()

    # Optional: NIC2
    doc.add_heading('Optional: NIC2 für Management', 1)

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Separates Management-Netzwerk über zweite Netzwerkkarte einrichten.')

    doc.add_heading('M.1 Hardware-Voraussetzungen', 3)
    doc.add_paragraph('Zweite physische Netzwerkkarte im Server', style='List Bullet')
    doc.add_paragraph('Separater Switch/VLAN für Management', style='List Bullet')
    doc.add_paragraph('Getrenntes IP-Subnetz (z.B. 192.168.2.0/24)', style='List Bullet')

    doc.add_heading('M.2 Management-Bridge erstellen', 3)
    doc.add_paragraph('1. GUI: Node → Network → Create → Linux Bridge', style='List Number')
    doc.add_paragraph('2. Name: vmbr1', style='List Number')
    doc.add_paragraph('3. IPv4/CIDR: 192.168.2.10/24', style='List Number')
    doc.add_paragraph('4. Bridge ports: enp0s32f7 (zweite NIC)', style='List Number')
    doc.add_paragraph('5. Comment: Management Network', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')

    doc.add_page_break()

    # Anhang
    doc.add_heading('Anhang: Nützliche Befehle', 1)

    doc.add_heading('System', 2)
    code = doc.add_paragraph(
        '# Proxmox Version\n'
        'pveversion -v\n\n'
        '# System-Ressourcen\n'
        'pvesh get /nodes/localhost/status\n\n'
        '# Cluster-Status (falls Cluster)\n'
        'pvecm status',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('VM/Container', 2)
    code = doc.add_paragraph(
        '# VM-Konfiguration anzeigen\n'
        'qm config 100\n\n'
        '# Container-Konfiguration\n'
        'pct config 200\n\n'
        '# VM klonen\n'
        'qm clone 100 101 --name clone-vm',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('Storage', 2)
    code = doc.add_paragraph(
        '# Storage-Status\n'
        'pvesm status\n\n'
        '# LVM-Status\n'
        'lvs\n'
        'vgs\n'
        'pvs',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # Troubleshooting
    doc.add_heading('Troubleshooting', 1)

    doc.add_heading('Proxmox Web-Interface nicht erreichbar', 2)
    code = doc.add_paragraph(
        '# Service-Status prüfen\n'
        'systemctl status pveproxy\n'
        'systemctl status pvedaemon\n\n'
        '# Neustart\n'
        'systemctl restart pveproxy\n'
        'systemctl restart pvedaemon\n\n'
        '# Logs prüfen\n'
        'journalctl -u pveproxy -f',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_heading('VM startet nicht', 2)
    code = doc.add_paragraph(
        '# Status prüfen\n'
        'qm status 100\n\n'
        '# Konfiguration prüfen\n'
        'qm config 100\n\n'
        '# Im Zweifelsfall: Snapshot zurückrollen',
        style='Normal'
    )
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_page_break()

    # Best Practices
    doc.add_heading('Best Practices', 1)

    doc.add_paragraph('1. Regelmäßige Backups: Mindestens täglich, 3-2-1 Regel', style='List Number')
    doc.add_paragraph('2. Updates: Monatlich, nach Test auf Test-System', style='List Number')
    doc.add_paragraph('3. Monitoring: Ressourcen-Nutzung überwachen', style='List Number')
    doc.add_paragraph('4. Dokumentation: Alle Änderungen dokumentieren', style='List Number')
    doc.add_paragraph('5. Snapshots: Vor jeder Änderung Snapshot erstellen', style='List Number')
    doc.add_paragraph('6. Sicherheit: Firewall, 2FA, SSH-Keys, getrennte Netze', style='List Number')
    doc.add_paragraph('7. Ressourcen-Limits: Für alle VMs/Container setzen', style='List Number')
    doc.add_paragraph('8. High Availability: Bei kritischen Systemen Cluster verwenden', style='List Number')

    doc.add_heading('Weiterführende Ressourcen', 2)

    p = doc.add_paragraph('Offizielle Dokumentation: ')
    add_hyperlink(p, 'https://pve.proxmox.com/pve-docs/', 'https://pve.proxmox.com/pve-docs/')

    p = doc.add_paragraph('Proxmox Forum: ')
    add_hyperlink(p, 'https://forum.proxmox.com/', 'https://forum.proxmox.com/')

    p = doc.add_paragraph('Proxmox Wiki: ')
    add_hyperlink(p, 'https://pve.proxmox.com/wiki/', 'https://pve.proxmox.com/wiki/')

    p = doc.add_paragraph()
    p.add_run('YouTube Kanäle:').bold = True
    doc.add_paragraph('Learn Linux TV', style='List Bullet')
    doc.add_paragraph('Techno Tim', style='List Bullet')
    doc.add_paragraph('Craft Computing', style='List Bullet')

    # Save document
    doc.save('/home/runner/work/agenten/agenten/Proxmox-Server-Anleitung.docx')
    print("Word-Dokument erfolgreich erstellt: Proxmox-Server-Anleitung.docx")

if __name__ == '__main__':
    create_word_document()
