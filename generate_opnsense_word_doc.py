#!/usr/bin/env python3
"""
Generate a comprehensive Word document for OPNsense on Proxmox
with extensive network diagrams and visual explanations.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import io
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    """Get fonts with fallback"""
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        return font_large, font_medium, font_small
    except:
        font = ImageFont.load_default()
        return font, font, font

def draw_box(draw, x, y, w, h, color, fill_alpha=30, text="", font=None, text_lines=None):
    """Draw a box with optional text"""
    # Draw rectangle
    draw.rectangle([x, y, x+w, y+h], outline=color, fill=color + (fill_alpha,), width=3)

    # Draw text
    if text and font:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((x + (w - text_width) // 2, y + 10), text, fill=(0, 0, 0), font=font)

    # Draw multiple text lines
    if text_lines and font:
        y_offset = 15
        for line in text_lines:
            draw.text((x + 10, y + y_offset), line, fill=(0, 0, 0), font=font)
            y_offset += 25

def draw_connection(draw, x1, y1, x2, y2, color=(100, 100, 100), width=3, dashed=False):
    """Draw a connection line"""
    if dashed:
        # Draw dashed line
        length = ((x2-x1)**2 + (y2-y1)**2)**0.5
        dashes = int(length / 15)
        for i in range(dashes):
            if i % 2 == 0:
                t1 = i / dashes
                t2 = min((i + 0.5) / dashes, 1)
                draw.line([
                    x1 + (x2-x1)*t1, y1 + (y2-y1)*t1,
                    x1 + (x2-x1)*t2, y1 + (y2-y1)*t2
                ], fill=color, width=width)
    else:
        draw.line([x1, y1, x2, y2], fill=color, width=width)

def create_overview_diagram():
    """Create complete network overview with all components"""
    width, height = 1200, 900
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    # Title
    draw.text((width//2 - 200, 20), "OPNsense auf Proxmox - Vollständige Netzwerk-Architektur",
              fill=(0, 0, 0), font=font_large)

    # Colors
    wan_color = (231, 76, 60)      # Red
    lan_color = (46, 204, 113)     # Green
    mgmt_color = (155, 89, 182)    # Purple
    vpn_color = (52, 152, 219)     # Blue
    proxmox_color = (230, 126, 34) # Orange

    # Internet cloud
    draw.ellipse([500, 70, 700, 150], outline=wan_color, width=4)
    draw.text((560, 100), "Internet", fill=(0, 0, 0), font=font_medium)

    # Router/Modem
    draw_box(draw, 480, 200, 240, 80, wan_color, text_lines=[
        "Router/Modem",
        "192.168.178.1"
    ], font=font_small)
    draw_connection(draw, 600, 150, 600, 200, wan_color)

    # Proxmox Host (large box)
    draw_box(draw, 100, 350, 1000, 480, proxmox_color, 20)
    draw.text((110, 360), "Proxmox VE Host", fill=(0, 0, 0), font=font_large)

    # Network Bridges
    bridge_y = 420

    # vmbr0 (WAN)
    draw_box(draw, 130, bridge_y, 180, 70, wan_color, text_lines=[
        "vmbr0 (WAN)",
        "nic0",
        "192.168.178.220"
    ], font=font_small)

    # vmbr1 (OPNsense WAN)
    draw_box(draw, 340, bridge_y, 180, 70, wan_color, text_lines=[
        "vmbr1",
        "nic1",
        "OPNsense WAN"
    ], font=font_small)

    # vmbr_LAN (Internal LAN)
    draw_box(draw, 550, bridge_y, 180, 70, lan_color, text_lines=[
        "vmbr_LAN",
        "intern",
        "192.168.10.0/24"
    ], font=font_small)

    # vmbr_MGMT (Management)
    draw_box(draw, 760, bridge_y, 180, 70, mgmt_color, text_lines=[
        "vmbr_MGMT",
        "nic2 (opt)",
        "192.168.50.0/24"
    ], font=font_small)

    # Connection from Router to vmbr0
    draw_connection(draw, 600, 280, 220, bridge_y, wan_color)

    # Connection from vmbr0 to vmbr1
    draw_connection(draw, 310, bridge_y + 35, 340, bridge_y + 35, wan_color)

    # OPNsense VM
    opn_y = 550
    draw_box(draw, 340, opn_y, 390, 120, (192, 57, 43), text_lines=[
        "OPNsense Firewall VM",
        "WAN: vmbr1 (DHCP)",
        "LAN: vmbr_LAN (192.168.10.1)",
        "MGMT: vmbr_MGMT (192.168.50.1)"
    ], font=font_small)

    # Connections to OPNsense
    draw_connection(draw, 430, bridge_y + 70, 430, opn_y, wan_color)  # WAN
    draw_connection(draw, 640, bridge_y + 70, 640, opn_y, lan_color)  # LAN
    draw_connection(draw, 850, bridge_y + 70, 720, opn_y, mgmt_color, dashed=True)  # MGMT

    # VMs in LAN
    vm_y = 720
    draw_box(draw, 560, vm_y, 160, 80, lan_color, text_lines=[
        "VMs / Container",
        "192.168.10.x",
        "via OPNsense"
    ], font=font_small)
    draw_connection(draw, 640, opn_y + 120, 640, vm_y, lan_color)

    # WireGuard VPN indicator
    draw_box(draw, 900, 550, 180, 80, vpn_color, text_lines=[
        "WireGuard VPN",
        "wg0",
        "10.10.10.1/24"
    ], font=font_small)
    draw_connection(draw, 730, opn_y + 60, 900, 590, vpn_color, dashed=True)

    # Legend
    legend_x = 120
    legend_y = 720
    draw.text((legend_x, legend_y), "Legende:", fill=(0, 0, 0), font=font_medium)

    draw.rectangle([legend_x, legend_y + 30, legend_x + 30, legend_y + 50], outline=wan_color, fill=wan_color, width=2)
    draw.text((legend_x + 40, legend_y + 32), "WAN / Internet", fill=(0, 0, 0), font=font_small)

    draw.rectangle([legend_x, legend_y + 60, legend_x + 30, legend_y + 80], outline=lan_color, fill=lan_color, width=2)
    draw.text((legend_x + 40, legend_y + 62), "LAN / Intern", fill=(0, 0, 0), font=font_small)

    draw.rectangle([legend_x, legend_y + 90, legend_x + 30, legend_y + 110], outline=mgmt_color, fill=mgmt_color, width=2)
    draw.text((legend_x + 40, legend_y + 92), "Management (Optional)", fill=(0, 0, 0), font=font_small)

    draw.rectangle([legend_x + 250, legend_y + 30, legend_x + 280, legend_y + 50], outline=vpn_color, fill=vpn_color, width=2)
    draw.text((legend_x + 290, legend_y + 32), "VPN", fill=(0, 0, 0), font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone1_diagram():
    """Milestone I: Preparation"""
    width, height = 900, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((250, 30), "Milestone I: Vorbereitung", fill=(0, 0, 0), font=font_large)

    # Three preparation boxes
    box_y = 120

    # Backup
    draw_box(draw, 50, box_y, 250, 180, (231, 76, 60), text_lines=[
        "1. Backup erstellen",
        "",
        "• Proxmox-Konfiguration",
        "• VM/Container-Backups",
        "• Netzwerk-Einstellungen",
        "• Dokumentation"
    ], font=font_small)

    # Documentation
    draw_box(draw, 330, box_y, 250, 180, (230, 126, 34), text_lines=[
        "2. Dokumentation",
        "",
        "• IP-Adressen planen",
        "• NIC-Zuordnung",
        "• VLAN-Schema",
        "• Rollback-Plan"
    ], font=font_small)

    # ISO Download
    draw_box(draw, 610, box_y, 250, 180, (46, 204, 113), text_lines=[
        "3. ISO herunterladen",
        "",
        "• OPNsense ISO",
        "• auf Proxmox laden",
        "• in local speichern"
    ], font=font_small)

    # Current state
    draw.text((50, 350), "Aktueller Zustand:", fill=(0, 0, 0), font=font_medium)
    draw_box(draw, 50, 390, 800, 150, (52, 73, 94), text_lines=[
        "Proxmox Host mit bestehendem Netzwerk:",
        "",
        "• nic0 → vmbr0 → Direkte Internet-Verbindung (192.168.178.220)",
        "• VMs nutzen vmbr0 für Netzwerk",
        "• Alle Geräte im gleichen Netzwerk wie Router (unsegmentiert)"
    ], font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone2_diagram():
    """Milestone II: Proxmox Network Setup"""
    width, height = 1000, 700
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((200, 30), "Milestone II: Proxmox Netzwerk-Bridges", fill=(0, 0, 0), font=font_large)

    # Physical NICs
    draw.text((50, 100), "Physische NICs:", fill=(0, 0, 0), font=font_medium)

    nic_y = 140
    draw_box(draw, 50, nic_y, 150, 60, (100, 100, 100), text_lines=[
        "nic0",
        "Physical"
    ], font=font_small)

    draw_box(draw, 220, nic_y, 150, 60, (100, 100, 100), text_lines=[
        "nic1",
        "Physical"
    ], font=font_small)

    draw_box(draw, 390, nic_y, 150, 60, (100, 100, 100), text_lines=[
        "nic2 (opt)",
        "Physical"
    ], font=font_small)

    # Arrow down
    draw_connection(draw, 125, 200, 125, 250, (0, 0, 0))
    draw_connection(draw, 295, 200, 295, 250, (0, 0, 0))
    draw_connection(draw, 465, 200, 465, 250, (0, 0, 0))

    # Bridges to create
    draw.text((50, 260), "Zu erstellende Bridges:", fill=(0, 0, 0), font=font_medium)

    bridge_y = 300

    # vmbr0 (existing)
    draw_box(draw, 50, bridge_y, 180, 100, (231, 76, 60), text_lines=[
        "vmbr0",
        "nic0",
        "WAN/Temp MGMT",
        "192.168.178.220"
    ], font=font_small)
    draw.text((60, bridge_y - 20), "✓ Vorhanden", fill=(46, 204, 113), font=font_small)

    # vmbr1 (new)
    draw_box(draw, 260, bridge_y, 180, 100, (230, 126, 34), text_lines=[
        "vmbr1",
        "nic1",
        "OPNsense WAN",
        "DHCP/Static"
    ], font=font_small)
    draw.text((270, bridge_y - 20), "⊕ Neu anlegen", fill=(52, 152, 219), font=font_small)

    # vmbr_LAN (new, internal)
    draw_box(draw, 470, bridge_y, 180, 100, (46, 204, 113), text_lines=[
        "vmbr_LAN",
        "intern (kein NIC)",
        "OPNsense LAN",
        "192.168.10.0/24"
    ], font=font_small)
    draw.text((480, bridge_y - 20), "⊕ Neu anlegen", fill=(52, 152, 219), font=font_small)

    # vmbr_MGMT (new, optional)
    draw_box(draw, 680, bridge_y, 180, 100, (155, 89, 182), text_lines=[
        "vmbr_MGMT",
        "nic2 (optional)",
        "Management",
        "192.168.50.0/24"
    ], font=font_small)
    draw.text((690, bridge_y - 20), "⊕ Optional", fill=(155, 89, 182), font=font_small)

    # CLI commands
    draw.text((50, 450), "Befehle in Proxmox (Node → Network → Create):", fill=(0, 0, 0), font=font_medium)

    cmd_box = draw_box(draw, 50, 490, 900, 160, (52, 73, 94), 10)
    draw.text((60, 500), "# vmbr1 erstellen (über GUI oder /etc/network/interfaces)", fill=(255, 255, 255), font=font_small)
    draw.text((60, 525), "auto vmbr1", fill=(255, 255, 255), font=font_small)
    draw.text((60, 545), "iface vmbr1 inet manual", fill=(255, 255, 255), font=font_small)
    draw.text((60, 565), "    bridge-ports nic1", fill=(255, 255, 255), font=font_small)
    draw.text((60, 585), "    bridge-stp off", fill=(255, 255, 255), font=font_small)
    draw.text((60, 605), "    bridge-fd 0", fill=(255, 255, 255), font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone3_diagram():
    """Milestone III: OPNsense VM Creation"""
    width, height = 1000, 800
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((250, 30), "Milestone III: OPNsense VM erstellen", fill=(0, 0, 0), font=font_large)

    # VM Configuration
    draw.text((50, 100), "VM-Konfiguration:", fill=(0, 0, 0), font=font_medium)

    config_y = 140
    draw_box(draw, 50, config_y, 900, 200, (192, 57, 43), 15)

    draw.text((70, config_y + 10), "OPNsense Firewall VM - Empfohlene Einstellungen", fill=(0, 0, 0), font=font_medium)
    draw.text((70, config_y + 40), "• VM ID: 100 (oder frei wählbar)", fill=(0, 0, 0), font=font_small)
    draw.text((70, config_y + 65), "• CPU: 2 Cores (Type: host)", fill=(0, 0, 0), font=font_small)
    draw.text((70, config_y + 90), "• RAM: 2048 MB (min. 1024 MB)", fill=(0, 0, 0), font=font_small)
    draw.text((70, config_y + 115), "• Disk: 20 GB (SSD empfohlen)", fill=(0, 0, 0), font=font_small)
    draw.text((70, config_y + 140), "• OS: BSD", fill=(0, 0, 0), font=font_small)
    draw.text((70, config_y + 165), "• ISO: OPNsense-XX.X-amd64.iso", fill=(0, 0, 0), font=font_small)

    # Network interfaces
    draw.text((50, 370), "Netzwerk-Interfaces der VM:", fill=(0, 0, 0), font=font_medium)

    nic_y = 410

    # WAN interface
    draw_box(draw, 50, nic_y, 280, 90, (231, 76, 60), text_lines=[
        "net0 (WAN)",
        "Bridge: vmbr1",
        "Model: VirtIO",
        "MAC: auto"
    ], font=font_small)

    # LAN interface
    draw_box(draw, 360, nic_y, 280, 90, (46, 204, 113), text_lines=[
        "net1 (LAN)",
        "Bridge: vmbr_LAN",
        "Model: VirtIO",
        "MAC: auto"
    ], font=font_small)

    # MGMT interface (optional)
    draw_box(draw, 670, nic_y, 280, 90, (155, 89, 182), text_lines=[
        "net2 (MGMT) - Optional",
        "Bridge: vmbr_MGMT",
        "Model: VirtIO",
        "MAC: auto"
    ], font=font_small)

    # Installation steps
    draw.text((50, 530), "Installation (nach VM-Start):", fill=(0, 0, 0), font=font_medium)

    steps_y = 570
    draw_box(draw, 50, steps_y, 900, 180, (52, 73, 94), 10)

    draw.text((70, steps_y + 10), "1. OPNsense Installer starten (Login: installer / opnsense)", fill=(255, 255, 255), font=font_small)
    draw.text((70, steps_y + 35), "2. Keymap: de (Deutsch) oder us (English)", fill=(255, 255, 255), font=font_small)
    draw.text((70, steps_y + 60), "3. Installation auf Disk durchführen (UFS oder ZFS)", fill=(255, 255, 255), font=font_small)
    draw.text((70, steps_y + 85), "4. Nach Neustart: WAN Interface zuweisen (vtnet0)", fill=(255, 255, 255), font=font_small)
    draw.text((70, steps_y + 110), "5. LAN Interface zuweisen (vtnet1) → IP: 192.168.10.1/24", fill=(255, 255, 255), font=font_small)
    draw.text((70, steps_y + 135), "6. Web-GUI: https://192.168.10.1 (root / opnsense)", fill=(255, 255, 255), font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone4_diagram():
    """Milestone IV: LAN Migration"""
    width, height = 1100, 800
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((250, 30), "Milestone IV: LAN Migration (schrittweise)", fill=(0, 0, 0), font=font_large)

    # Before state
    draw.text((50, 100), "VORHER (Alt):", fill=(231, 76, 60), font=font_medium)
    draw_box(draw, 50, 140, 480, 150, (231, 76, 60), 15)
    draw.text((70, 155), "Router 192.168.178.1", fill=(0, 0, 0), font=font_small)
    draw.text((90, 180), "↓", fill=(0, 0, 0), font=font_medium)
    draw.text((70, 200), "Proxmox vmbr0 (192.168.178.220)", fill=(0, 0, 0), font=font_small)
    draw.text((90, 225), "↓", fill=(0, 0, 0), font=font_medium)
    draw.text((70, 245), "VMs direkt am Router-Netz", fill=(0, 0, 0), font=font_small)
    draw.text((70, 265), "(keine Firewall-Segmentierung)", fill=(231, 76, 60), font=font_small)

    # Arrow
    draw.text((560, 200), "→→→", fill=(0, 0, 0), font=font_large)

    # After state
    draw.text((620, 100), "NACHHER (Neu):", fill=(46, 204, 113), font=font_medium)
    draw_box(draw, 620, 140, 450, 150, (46, 204, 113), 15)
    draw.text((640, 155), "Router 192.168.178.1", fill=(0, 0, 0), font=font_small)
    draw.text((660, 180), "↓", fill=(0, 0, 0), font=font_medium)
    draw.text((640, 200), "OPNsense WAN (vmbr1)", fill=(0, 0, 0), font=font_small)
    draw.text((660, 225), "↓ Firewall ↓", fill=(192, 57, 43), font=font_small)
    draw.text((640, 245), "OPNsense LAN (192.168.10.1)", fill=(0, 0, 0), font=font_small)
    draw.text((660, 270), "↓", fill=(0, 0, 0), font=font_medium)
    draw.text((640, 265), "VMs via vmbr_LAN (segmentiert)", fill=(46, 204, 113), font=font_small)

    # Migration steps
    draw.text((50, 330), "Migrations-Schritte:", fill=(0, 0, 0), font=font_medium)

    step_y = 370

    # Step 1
    draw.text((70, step_y), "1", fill=(255, 255, 255), font=font_medium)
    draw.ellipse([60, step_y - 5, 90, step_y + 25], fill=(230, 126, 34), outline=(230, 126, 34))
    draw_box(draw, 110, step_y - 10, 950, 60, (230, 126, 34), 10, text_lines=[
        "Test-VM erstellen auf vmbr_LAN (192.168.10.100)",
        "DHCP/DNS von OPNsense testen"
    ], font=font_small)

    # Step 2
    step_y += 75
    draw.text((70, step_y), "2", fill=(255, 255, 255), font=font_medium)
    draw.ellipse([60, step_y - 5, 90, step_y + 25], fill=(241, 196, 15), outline=(241, 196, 15))
    draw_box(draw, 110, step_y - 10, 950, 60, (241, 196, 15), 10, text_lines=[
        "DHCP Server in OPNsense konfigurieren (Services → DHCPv4 → LAN)",
        "Range: 192.168.10.100 - 192.168.10.200, DNS: 192.168.10.1"
    ], font=font_small)

    # Step 3
    step_y += 75
    draw.text((70, step_y), "3", fill=(255, 255, 255), font=font_medium)
    draw.ellipse([60, step_y - 5, 90, step_y + 25], fill=(52, 152, 219), outline=(52, 152, 219))
    draw_box(draw, 110, step_y - 10, 950, 60, (52, 152, 219), 10, text_lines=[
        "Firewall-Regeln erstellen (Firewall → Rules → LAN)",
        "Standard: LAN → WAN erlauben, LAN → Internet erlauben"
    ], font=font_small)

    # Step 4
    step_y += 75
    draw.text((70, step_y), "4", fill=(255, 255, 255), font=font_medium)
    draw.ellipse([60, step_y - 5, 90, step_y + 25], fill=(46, 204, 113), outline=(46, 204, 113))
    draw_box(draw, 110, step_y - 10, 950, 60, (46, 204, 113), 10, text_lines=[
        "VMs einzeln migrieren: VM ausschalten → Network Device auf vmbr_LAN ändern",
        "VM starten → IP via DHCP prüfen → Konnektivität testen"
    ], font=font_small)

    # Warning box
    draw_box(draw, 50, 680, 1000, 80, (231, 76, 60), 15)
    draw.text((70, 695), "⚠ WICHTIG: Proxmox Host bleibt auf vmbr0!", fill=(0, 0, 0), font=font_medium)
    draw.text((70, 720), "Erst in Milestone VI wird Proxmox auf Management-Netzwerk (vmbr_MGMT) verschoben.", fill=(0, 0, 0), font=font_small)
    draw.text((70, 740), "So bleibt der Zugriff auf Proxmox während der Migration erhalten.", fill=(0, 0, 0), font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone5_diagram():
    """Milestone V: WireGuard VPN"""
    width, height = 900, 700
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((200, 30), "Milestone V: WireGuard VPN einrichten", fill=(0, 0, 0), font=font_large)

    # VPN Topology
    draw.text((50, 100), "VPN-Topologie:", fill=(0, 0, 0), font=font_medium)

    # Internet
    draw.ellipse([350, 140, 550, 200], outline=(231, 76, 60), width=3)
    draw.text((410, 160), "Internet", fill=(0, 0, 0), font=font_medium)

    # OPNsense
    draw_box(draw, 300, 260, 300, 100, (52, 152, 219), text_lines=[
        "OPNsense mit WireGuard",
        "Public IP / DynDNS",
        "Port: 51820 (UDP)"
    ], font=font_small)
    draw_connection(draw, 450, 200, 450, 260, (231, 76, 60))

    # WireGuard tunnel
    draw.text((380, 380), "WireGuard Tunnel", fill=(52, 152, 219), font=font_medium)
    draw.text((380, 405), "10.10.10.0/24", fill=(52, 152, 219), font=font_small)

    # Remote client
    draw_box(draw, 50, 480, 200, 100, (46, 204, 113), text_lines=[
        "Remote Client",
        "(Laptop/Handy)",
        "10.10.10.2"
    ], font=font_small)
    draw_connection(draw, 150, 480, 350, 360, (52, 152, 219), width=3, dashed=True)

    # Another client
    draw_box(draw, 650, 480, 200, 100, (46, 204, 113), text_lines=[
        "Remote Client 2",
        "(Home Office)",
        "10.10.10.3"
    ], font=font_small)
    draw_connection(draw, 750, 480, 550, 360, (52, 152, 219), width=3, dashed=True)

    # Setup steps
    draw.text((50, 610), "Einrichtung in OPNsense:", fill=(0, 0, 0), font=font_medium)
    draw.text((70, 640), "1. System → Firmware → Plugins → os-wireguard installieren", fill=(0, 0, 0), font=font_small)
    draw.text((70, 660), "2. VPN → WireGuard → Instances → Server erstellen (Port 51820)", fill=(0, 0, 0), font=font_small)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_nic_assignment_table():
    """Create NIC assignment table as image"""
    width, height = 1000, 500
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    font_large, font_medium, font_small = get_fonts()

    draw.text((250, 30), "NIC-Zuordnung (Zielkonfiguration)", fill=(0, 0, 0), font=font_large)

    # Table header
    header_y = 100
    col_widths = [150, 200, 300, 250]
    col_x = [50, 200, 400, 700]

    headers = ["Physische NIC", "Bridge (Proxmox)", "Zweck", "IP (Beispiel)"]

    # Draw header
    for i, (x, w, text) in enumerate(zip(col_x, col_widths, headers)):
        draw.rectangle([x, header_y, x + w, header_y + 40], outline=(52, 73, 94), fill=(52, 73, 94), width=2)
        draw.text((x + 10, header_y + 10), text, fill=(255, 255, 255), font=font_medium)

    # Table rows
    rows = [
        ("nic0", "vmbr0", "WAN + temp. Proxmox MGMT", "192.168.178.220/24", (231, 76, 60)),
        ("nic1", "vmbr1", "OPNsense WAN (an Switch/Router)", "via DHCP / statisch", (230, 126, 34)),
        ("nic1 intern", "vmbr_LAN", "Internes LAN hinter OPNsense", "192.168.10.0/24", (46, 204, 113)),
        ("nic2 (optional)", "vmbr_MGMT", "Isoliertes MGMT-Netz", "192.168.50.0/24", (155, 89, 182)),
        ("—", "wg0", "WireGuard VPN (Host)", "10.10.10.1/24", (52, 152, 219)),
    ]

    row_y = header_y + 40
    for row_data in rows:
        nic, bridge, purpose, ip, color = row_data
        row_height = 60

        # Draw cells
        for i, (x, w) in enumerate(zip(col_x, col_widths)):
            draw.rectangle([x, row_y, x + w, row_y + row_height], outline=color, fill=color + (30,), width=2)

        # Draw text
        draw.text((col_x[0] + 10, row_y + 20), nic, fill=(0, 0, 0), font=font_small)
        draw.text((col_x[1] + 10, row_y + 20), bridge, fill=(0, 0, 0), font=font_small)
        draw.text((col_x[2] + 10, row_y + 15), purpose, fill=(0, 0, 0), font=font_small)
        draw.text((col_x[3] + 10, row_y + 20), ip, fill=(0, 0, 0), font=font_small)

        row_y += row_height

    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io

def create_milestone_icon(number, color):
    """Create milestone icon"""
    size = 100
    img = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    draw.ellipse([10, 10, 90, 90], outline=color, fill=color, width=3)
    text = str(number)
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
    """Add hyperlink to paragraph"""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

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
    """Create comprehensive OPNsense Word document"""
    doc = Document()

    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title page
    title = doc.add_heading('OPNsense auf Proxmox', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.color.rgb = RGBColor(192, 57, 43)
    title.runs[0].font.size = Pt(42)

    subtitle = doc.add_paragraph('Netzwerk-Segmentierung mit Firewall')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(20)
    subtitle.runs[0].font.color.rgb = RGBColor(52, 73, 94)

    subtitle2 = doc.add_paragraph('Schritt-für-Schritt Anleitung mit ausführlichen Diagrammen')
    subtitle2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle2.runs[0].font.size = Pt(14)
    subtitle2.runs[0].font.color.rgb = RGBColor(127, 140, 141)

    doc.add_paragraph()

    # Overview diagram on title page
    overview_img = create_overview_diagram()
    doc.add_picture(overview_img, width=Inches(6))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()
    version = doc.add_paragraph()
    version.alignment = WD_ALIGN_PARAGRAPH.CENTER
    version.add_run('Version 1.0 | Mai 2026').font.size = Pt(11)

    doc.add_page_break()

    # Table of contents
    toc = doc.add_heading('Inhaltsverzeichnis', 1)
    toc.runs[0].font.color.rgb = RGBColor(41, 128, 185)

    toc_items = [
        ('Milestone I', 'Vorbereitung - Backup, Dokumentation, ISO-Download'),
        ('Milestone II', 'Proxmox Netzwerk - Bridges anlegen, NICs zuweisen'),
        ('Milestone III', 'OPNsense VM - VM erstellen, installieren, Grundkonfiguration'),
        ('Milestone IV', 'LAN migrieren - Test-VM, DHCP/DNS, schrittweise Migration'),
        ('Milestone V', 'WireGuard VPN - Plugin, Tunnel, Firewall-Regeln'),
        ('Milestone VI', 'MGMT-Netz - nic2, vmbr_MGMT, Proxmox isolieren (Optional)'),
        ('Milestone VII', 'Härtung & Erweiterungen - IDS/IPS, VLANs (Optional)'),
        ('Anhang', 'NIC-Zuordnung, Troubleshooting, Best Practices')
    ]

    for milestone, desc in toc_items:
        p = doc.add_paragraph()
        p.add_run(f'{milestone}: ').bold = True
        p.add_run(desc)
        p.style = 'List Bullet'
        p.runs[0].font.size = Pt(12)

    doc.add_page_break()

    # NIC Assignment Overview
    doc.add_heading('NIC-Zuordnung (Überblick)', 1)
    nic_table_img = create_nic_assignment_table()
    doc.add_picture(nic_table_img, width=Inches(6.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    p = doc.add_paragraph()
    p.add_run('Wichtige Hinweise:').bold = True
    doc.add_paragraph('vmbr_LAN ist eine interne Bridge ohne physisches NIC', style='List Bullet')
    doc.add_paragraph('nic2 und vmbr_MGMT sind optional für zusätzliche Sicherheit', style='List Bullet')
    doc.add_paragraph('WireGuard (wg0) ist ein virtuelles VPN-Interface', style='List Bullet')

    doc.add_page_break()

    # Milestone colors
    colors = [
        (231, 76, 60),   # I - Red
        (230, 126, 34),  # II - Orange
        (241, 196, 15),  # III - Yellow
        (46, 204, 113),  # IV - Green
        (52, 152, 219),  # V - Blue
        (155, 89, 182),  # VI - Purple
        (52, 73, 94),    # VII - Dark
    ]

    # Milestone I
    doc.add_heading('Milestone I: Vorbereitung', 1)
    icon1 = create_milestone_icon('I', colors[0])
    doc.add_picture(icon1, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Backup erstellen, Netzwerk dokumentieren und ISO-Image bereitstellen.')

    m1_img = create_milestone1_diagram()
    doc.add_picture(m1_img, width=Inches(6))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('1.1 Backup erstellen (WICHTIG!)', 4)
    doc.add_paragraph('Proxmox-Konfiguration sichern:', style='List Bullet')
    code = doc.add_paragraph('cp -r /etc/network /root/backup-network-$(date +%Y%m%d)', style='Normal')
    code.runs[0].font.name = 'Courier New'
    code.runs[0].font.size = Pt(9)

    doc.add_paragraph('VM-Backups erstellen (GUI: Datacenter → Backup)', style='List Bullet')
    doc.add_paragraph('Aktuelle Netzwerk-Konfiguration dokumentieren', style='List Bullet')

    doc.add_heading('1.2 Netzwerk-Planung dokumentieren', 4)
    doc.add_paragraph('IP-Adressbereiche festlegen:', style='List Bullet')
    doc.add_paragraph('WAN: 192.168.178.0/24 (Router-Netz)', style='List Bullet 2')
    doc.add_paragraph('LAN (neu): 192.168.10.0/24 (OPNsense LAN)', style='List Bullet 2')
    doc.add_paragraph('MGMT (optional): 192.168.50.0/24 (Management)', style='List Bullet 2')
    doc.add_paragraph('VPN: 10.10.10.0/24 (WireGuard)', style='List Bullet 2')

    doc.add_paragraph('NIC-Zuordnung planen (siehe NIC-Tabelle)', style='List Bullet')
    doc.add_paragraph('Rollback-Strategie definieren', style='List Bullet')

    doc.add_heading('1.3 OPNsense ISO herunterladen', 4)
    p = doc.add_paragraph('Download von: ')
    add_hyperlink(p, 'https://opnsense.org/download/', 'https://opnsense.org/download/')

    doc.add_paragraph('Architektur: amd64', style='List Bullet')
    doc.add_paragraph('Image Type: dvd (komplette Installation)', style='List Bullet')
    doc.add_paragraph('ISO auf Proxmox hochladen: local → ISO Images → Upload', style='List Bullet')

    doc.add_page_break()

    # Milestone II
    doc.add_heading('Milestone II: Proxmox Netzwerk-Bridges', 1)
    icon2 = create_milestone_icon('II', colors[1])
    doc.add_picture(icon2, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Netzwerk-Bridges in Proxmox erstellen und NICs zuordnen.')

    m2_img = create_milestone2_diagram()
    doc.add_picture(m2_img, width=Inches(6.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('2.1 Bestehende Konfiguration prüfen', 4)
    doc.add_paragraph('GUI: Node → Network', style='List Bullet')
    doc.add_paragraph('vmbr0 sollte bereits existieren (an nic0)', style='List Bullet')
    doc.add_paragraph('IP-Adresse notieren (z.B. 192.168.178.220)', style='List Bullet')

    doc.add_heading('2.2 vmbr1 erstellen (OPNsense WAN)', 4)
    doc.add_paragraph('1. Node → Network → Create → Linux Bridge', style='List Number')
    doc.add_paragraph('2. Name: vmbr1', style='List Number')
    doc.add_paragraph('3. IPv4/CIDR: leer lassen (keine IP auf Bridge)', style='List Number')
    doc.add_paragraph('4. Bridge ports: nic1 (zweite physische NIC)', style='List Number')
    doc.add_paragraph('5. Autostart: aktivieren', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')

    doc.add_heading('2.3 vmbr_LAN erstellen (Internes LAN)', 4)
    doc.add_paragraph('1. Node → Network → Create → Linux Bridge', style='List Number')
    doc.add_paragraph('2. Name: vmbr_LAN (oder vmbr2)', style='List Number')
    doc.add_paragraph('3. IPv4/CIDR: leer lassen', style='List Number')
    doc.add_paragraph('4. Bridge ports: LEER (keine physische NIC!)', style='List Number')
    doc.add_paragraph('5. Comment: Internal LAN behind OPNsense', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')

    p = doc.add_paragraph()
    p.add_run('Wichtig: ').bold = True
    p.add_run('vmbr_LAN ist eine rein virtuelle Bridge ohne physisches Interface. Alle VMs hinter der Firewall nutzen diese Bridge.')

    doc.add_heading('2.4 vmbr_MGMT erstellen (Optional - Management)', 4)
    doc.add_paragraph('1. Node → Network → Create → Linux Bridge', style='List Number')
    doc.add_paragraph('2. Name: vmbr_MGMT (oder vmbr3)', style='List Number')
    doc.add_paragraph('3. IPv4/CIDR: leer lassen', style='List Number')
    doc.add_paragraph('4. Bridge ports: nic2 (dritte NIC, falls vorhanden)', style='List Number')
    doc.add_paragraph('5. Comment: Isolated Management Network', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')

    doc.add_page_break()

    # Milestone III
    doc.add_heading('Milestone III: OPNsense VM erstellen', 1)
    icon3 = create_milestone_icon('III', colors[2])
    doc.add_picture(icon3, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('OPNsense Firewall VM erstellen, installieren und grundlegend konfigurieren.')

    m3_img = create_milestone3_diagram()
    doc.add_picture(m3_img, width=Inches(6.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('3.1 VM erstellen', 4)
    doc.add_paragraph('1. Rechtsklick auf Node → Create VM', style='List Number')
    doc.add_paragraph('2. General: VM ID 100, Name: OPNsense', style='List Number')
    doc.add_paragraph('3. OS: ISO Image auswählen, Guest OS: Other', style='List Number')
    doc.add_paragraph('4. System: Standard (BIOS: Default, SCSI Controller: VirtIO SCSI)', style='List Number')
    doc.add_paragraph('5. Disks: 20 GB, Storage: local-lvm, Cache: Write back', style='List Number')
    doc.add_paragraph('6. CPU: 2 Cores, Type: host', style='List Number')
    doc.add_paragraph('7. Memory: 2048 MB', style='List Number')
    doc.add_paragraph('8. Network: Bridge: vmbr1, Model: VirtIO', style='List Number')

    doc.add_heading('3.2 Zusätzliche Netzwerk-Interfaces hinzufügen', 4)
    doc.add_paragraph('Nach VM-Erstellung:', style='List Bullet')
    doc.add_paragraph('VM 100 → Hardware → Add → Network Device', style='List Bullet')
    doc.add_paragraph('net1: Bridge: vmbr_LAN, Model: VirtIO (LAN Interface)', style='List Bullet')
    doc.add_paragraph('Optional: net2: Bridge: vmbr_MGMT, Model: VirtIO', style='List Bullet')

    doc.add_heading('3.3 OPNsense Installation', 4)
    doc.add_paragraph('1. VM starten → Console öffnen', style='List Number')
    doc.add_paragraph('2. Login: installer / opnsense', style='List Number')
    doc.add_paragraph('3. Keymap: de (German) oder us (English) auswählen', style='List Number')
    doc.add_paragraph('4. Install (UFS): Guided installation auswählen', style='List Number')
    doc.add_paragraph('5. Installation durchführen (Stripe - keine Redundanz)', style='List Number')
    doc.add_paragraph('6. Root-Passwort setzen (sicheres Passwort!)', style='List Number')
    doc.add_paragraph('7. Complete Install → Reboot', style='List Number')
    doc.add_paragraph('8. ISO-Image entfernen: Hardware → CD/DVD → Do not use', style='List Number')

    doc.add_heading('3.4 Interface-Zuordnung', 4)
    doc.add_paragraph('Nach Neustart im Console:', style='List Bullet')
    doc.add_paragraph('1. Interfaces assign (Option 1)', style='List Number 2')
    doc.add_paragraph('2. WAN Interface: vtnet0 (an vmbr1)', style='List Number 2')
    doc.add_paragraph('3. LAN Interface: vtnet1 (an vmbr_LAN)', style='List Number 2')
    doc.add_paragraph('4. Optional Interfaces: vtnet2 (MGMT)', style='List Number 2')

    doc.add_heading('3.5 LAN IP konfigurieren', 4)
    doc.add_paragraph('Set interface IP address (Option 2):', style='List Bullet')
    doc.add_paragraph('Interface: 2 (LAN)', style='List Number 2')
    doc.add_paragraph('IPv4: 192.168.10.1/24', style='List Number 2')
    doc.add_paragraph('IPv6: none', style='List Number 2')
    doc.add_paragraph('DHCP Server: yes (Range: 192.168.10.100 - 192.168.10.200)', style='List Number 2')

    doc.add_heading('3.6 Web-GUI Zugriff', 4)
    doc.add_paragraph('Test-VM oder Laptop an vmbr_LAN anschließen', style='List Bullet')
    doc.add_paragraph('Browser öffnen: https://192.168.10.1', style='List Bullet')
    doc.add_paragraph('Login: root / <gesetztes Passwort>', style='List Bullet')
    doc.add_paragraph('Setup-Wizard durchlaufen', style='List Bullet')

    doc.add_page_break()

    # Milestone IV
    doc.add_heading('Milestone IV: LAN Migration', 1)
    icon4 = create_milestone_icon('IV', colors[3])
    doc.add_picture(icon4, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('VMs schrittweise von direktem Router-Zugang auf OPNsense-LAN migrieren.')

    m4_img = create_milestone4_diagram()
    doc.add_picture(m4_img, width=Inches(6.5))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('4.1 DHCP Server in OPNsense konfigurieren', 4)
    doc.add_paragraph('Services → DHCPv4 → [LAN]', style='List Bullet')
    doc.add_paragraph('Enable: aktivieren', style='List Bullet')
    doc.add_paragraph('Range: 192.168.10.100 - 192.168.10.200', style='List Bullet')
    doc.add_paragraph('DNS Servers: 192.168.10.1 (OPNsense)', style='List Bullet')
    doc.add_paragraph('Gateway: 192.168.10.1', style='List Bullet')
    doc.add_paragraph('Save', style='List Bullet')

    doc.add_heading('4.2 Firewall-Regeln erstellen', 4)
    doc.add_paragraph('Firewall → Rules → LAN', style='List Bullet')
    doc.add_paragraph('Add Rule:', style='List Bullet')
    doc.add_paragraph('Action: Pass', style='List Bullet 2')
    doc.add_paragraph('Interface: LAN', style='List Bullet 2')
    doc.add_paragraph('Protocol: any', style='List Bullet 2')
    doc.add_paragraph('Source: LAN net', style='List Bullet 2')
    doc.add_paragraph('Destination: any', style='List Bullet 2')
    doc.add_paragraph('Description: Allow LAN to any', style='List Bullet 2')
    doc.add_paragraph('Save → Apply Changes', style='List Bullet')

    doc.add_heading('4.3 Test-VM erstellen und testen', 4)
    doc.add_paragraph('1. Neue VM oder bestehende Test-VM nutzen', style='List Number')
    doc.add_paragraph('2. Network Device: vmbr_LAN', style='List Number')
    doc.add_paragraph('3. VM starten', style='List Number')
    doc.add_paragraph('4. IP-Adresse prüfen (sollte 192.168.10.x sein)', style='List Number')
    doc.add_paragraph('5. Internet-Zugriff testen: ping 8.8.8.8', style='List Number')
    doc.add_paragraph('6. DNS testen: ping google.com', style='List Number')

    doc.add_heading('4.4 VMs einzeln migrieren', 4)
    doc.add_paragraph('Für jede VM:', style='List Bullet')
    doc.add_paragraph('1. VM herunterfahren', style='List Number 2')
    doc.add_paragraph('2. Hardware → Network Device → Edit', style='List Number 2')
    doc.add_paragraph('3. Bridge: vmbr_LAN auswählen', style='List Number 2')
    doc.add_paragraph('4. OK → VM starten', style='List Number 2')
    doc.add_paragraph('5. Konnektivität testen', style='List Number 2')
    doc.add_paragraph('6. Nächste VM', style='List Number 2')

    p = doc.add_paragraph()
    p.add_run('⚠ WICHTIG: ').bold = True
    p.add_run('Proxmox Host NICHT migrieren! Der Host bleibt auf vmbr0 für Zugriff.')

    doc.add_page_break()

    # Milestone V
    doc.add_heading('Milestone V: WireGuard VPN', 1)
    icon5 = create_milestone_icon('V', colors[4])
    doc.add_picture(icon5, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('WireGuard VPN einrichten für sicheren Remote-Zugriff.')

    m5_img = create_milestone5_diagram()
    doc.add_picture(m5_img, width=Inches(6))
    last_paragraph = doc.paragraphs[-1]
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('5.1 WireGuard Plugin installieren', 4)
    doc.add_paragraph('1. System → Firmware → Plugins', style='List Number')
    doc.add_paragraph('2. Suche: wireguard', style='List Number')
    doc.add_paragraph('3. os-wireguard installieren (+)', style='List Number')
    doc.add_paragraph('4. Installation bestätigen', style='List Number')

    doc.add_heading('5.2 WireGuard Server konfigurieren', 4)
    doc.add_paragraph('VPN → WireGuard → Local', style='List Bullet')
    doc.add_paragraph('Add (+):', style='List Bullet')
    doc.add_paragraph('Name: wg0', style='List Bullet 2')
    doc.add_paragraph('Listen Port: 51820', style='List Bullet 2')
    doc.add_paragraph('Tunnel Address: 10.10.10.1/24', style='List Bullet 2')
    doc.add_paragraph('Peers: (noch keine)', style='List Bullet 2')
    doc.add_paragraph('Save', style='List Bullet')

    doc.add_heading('5.3 WireGuard Interface aktivieren', 4)
    doc.add_paragraph('VPN → WireGuard → Instances', style='List Bullet')
    doc.add_paragraph('Enable wg0 aktivieren', style='List Bullet')
    doc.add_paragraph('Apply', style='List Bullet')

    doc.add_heading('5.4 Firewall-Regeln für WireGuard', 4)
    doc.add_paragraph('Firewall → Rules → WAN', style='List Bullet')
    doc.add_paragraph('Add Rule:', style='List Bullet')
    doc.add_paragraph('Action: Pass', style='List Bullet 2')
    doc.add_paragraph('Protocol: UDP', style='List Bullet 2')
    doc.add_paragraph('Destination Port: 51820', style='List Bullet 2')
    doc.add_paragraph('Description: WireGuard VPN', style='List Bullet 2')
    doc.add_paragraph('Save → Apply', style='List Bullet')

    doc.add_heading('5.5 Client-Konfiguration', 4)
    doc.add_paragraph('VPN → WireGuard → Endpoints → Add', style='List Bullet')
    doc.add_paragraph('Name: client1', style='List Bullet')
    doc.add_paragraph('Public Key: (vom Client)', style='List Bullet')
    doc.add_paragraph('Allowed IPs: 10.10.10.2/32', style='List Bullet')
    doc.add_paragraph('QR-Code generieren für mobile Clients', style='List Bullet')

    doc.add_page_break()

    # Milestone VI
    doc.add_heading('Milestone VI: Management-Netz (Optional)', 1)
    icon6 = create_milestone_icon('VI', colors[5])
    doc.add_picture(icon6, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Proxmox Host auf isoliertes Management-Netzwerk verschieben für erhöhte Sicherheit.')

    p = doc.add_paragraph()
    p.add_run('Hinweis: ').bold = True
    p.add_run('Dieser Schritt ist optional und erfordert eine zweite physische NIC (nic2)!')

    doc.add_heading('Schritt-für-Schritt', 3)

    doc.add_heading('6.1 MGMT Interface in OPNsense konfigurieren', 4)
    doc.add_paragraph('Interfaces → Assignments', style='List Bullet')
    doc.add_paragraph('vtnet2 als MGMT zuweisen', style='List Bullet')
    doc.add_paragraph('Interfaces → [MGMT] → Enable', style='List Bullet')
    doc.add_paragraph('IPv4: 192.168.50.1/24', style='List Bullet')
    doc.add_paragraph('Save → Apply', style='List Bullet')

    doc.add_heading('6.2 Proxmox auf Management-Netz verschieben', 4)
    p = doc.add_paragraph()
    p.add_run('⚠ VORSICHT: ').bold = True
    p.add_run('SSH-Zugang vor Änderung sicherstellen!')

    doc.add_paragraph('1. Node → Network → vmbr0 bearbeiten', style='List Number')
    doc.add_paragraph('2. Alte IP entfernen', style='List Number')
    doc.add_paragraph('3. vmbr_MGMT erstellen/bearbeiten', style='List Number')
    doc.add_paragraph('4. IPv4/CIDR: 192.168.50.10/24', style='List Number')
    doc.add_paragraph('5. Gateway: 192.168.50.1', style='List Number')
    doc.add_paragraph('6. Apply Configuration', style='List Number')
    doc.add_paragraph('7. Neue IP: https://192.168.50.10:8006', style='List Number')

    doc.add_heading('6.3 Firewall-Regeln für MGMT', 4)
    doc.add_paragraph('In OPNsense: Firewall → Rules → MGMT', style='List Bullet')
    doc.add_paragraph('Nur notwendige Services erlauben (SSH, HTTPS)', style='List Bullet')
    doc.add_paragraph('Zugriff von MGMT → LAN blockieren (Isolation)', style='List Bullet')

    doc.add_page_break()

    # Milestone VII
    doc.add_heading('Milestone VII: Härtung & Erweiterungen (Optional)', 1)
    icon7 = create_milestone_icon('VII', colors[6])
    doc.add_picture(icon7, width=Inches(0.6))

    doc.add_heading('Ziel', 2)
    doc.add_paragraph('Zusätzliche Sicherheits-Features und erweiterte Funktionen.')

    doc.add_heading('7.1 IDS/IPS (Suricata)', 4)
    doc.add_paragraph('System → Firmware → Plugins → os-suricata', style='List Bullet')
    doc.add_paragraph('Services → Intrusion Detection → Administration', style='List Bullet')
    doc.add_paragraph('Pattern: ET Open Ruleset', style='List Bullet')
    doc.add_paragraph('Interfaces: WAN aktivieren', style='List Bullet')

    doc.add_heading('7.2 VLANs erstellen', 4)
    doc.add_paragraph('Interfaces → Other Types → VLAN', style='List Bullet')
    doc.add_paragraph('Parent Interface: LAN', style='List Bullet')
    doc.add_paragraph('VLAN Tag: 10 (z.B. für IoT)', style='List Bullet')
    doc.add_paragraph('Interfaces zuweisen und konfigurieren', style='List Bullet')

    doc.add_heading('7.3 Zenarmor (Web-Filter)', 4)
    doc.add_paragraph('System → Firmware → Plugins → os-sensei', style='List Bullet')
    doc.add_paragraph('Services → Sensei', style='List Bullet')
    doc.add_paragraph('Web-Filtering, Application Control aktivieren', style='List Bullet')

    doc.add_heading('7.4 HAProxy (Reverse Proxy)', 4)
    doc.add_paragraph('System → Firmware → Plugins → os-haproxy', style='List Bullet')
    doc.add_paragraph('Services → HAProxy', style='List Bullet')
    doc.add_paragraph('Backends und Frontends für Web-Services konfigurieren', style='List Bullet')

    doc.add_page_break()

    # Troubleshooting
    doc.add_heading('Troubleshooting', 1)

    doc.add_heading('Problem: Kein Internet nach Migration', 2)
    doc.add_paragraph('• OPNsense WAN-Interface prüfen (sollte IP haben)', style='List Bullet')
    doc.add_paragraph('• Gateway in OPNsense prüfen (System → Gateways)', style='List Bullet')
    doc.add_paragraph('• Firewall-Regeln prüfen (LAN → WAN erlauben)', style='List Bullet')
    doc.add_paragraph('• NAT prüfen (Firewall → NAT → Outbound)', style='List Bullet')

    doc.add_heading('Problem: VMs bekommen keine IP', 2)
    doc.add_paragraph('• DHCP Server in OPNsense aktiv? (Services → DHCPv4)', style='List Bullet')
    doc.add_paragraph('• VM an richtige Bridge? (vmbr_LAN)', style='List Bullet')
    doc.add_paragraph('• Firewall-Regel für DHCP (UDP 67/68)', style='List Bullet')

    doc.add_heading('Problem: Proxmox nicht erreichbar nach MGMT-Migration', 2)
    doc.add_paragraph('• Physisch an MGMT-Netz anschließen', style='List Bullet')
    doc.add_paragraph('• Über Console: /etc/network/interfaces prüfen', style='List Bullet')
    doc.add_paragraph('• Gateway auf 192.168.50.1 setzen', style='List Bullet')
    doc.add_paragraph('• Rollback: Backup einspielen aus Milestone I', style='List Bullet')

    doc.add_page_break()

    # Best Practices
    doc.add_heading('Best Practices', 1)

    doc.add_paragraph('1. Immer Backups vor Änderungen erstellen', style='List Number')
    doc.add_paragraph('2. Änderungen schrittweise durchführen (ein Milestone nach dem anderen)', style='List Number')
    doc.add_paragraph('3. Test-VMs für Validierung nutzen', style='List Number')
    doc.add_paragraph('4. Dokumentation aktuell halten (IP-Adressen, VLANs)', style='List Number')
    doc.add_paragraph('5. Firewall-Regeln restriktiv gestalten (nur notwendiges erlauben)', style='List Number')
    doc.add_paragraph('6. Regelmäßige Updates (OPNsense und Proxmox)', style='List Number')
    doc.add_paragraph('7. Monitoring aktivieren (OPNsense Insight, Proxmox Monitoring)', style='List Number')
    doc.add_paragraph('8. Separate Netze für verschiedene Zwecke (IoT, Server, Clients)', style='List Number')

    doc.add_heading('Weiterführende Ressourcen', 2)

    p = doc.add_paragraph('OPNsense Dokumentation: ')
    add_hyperlink(p, 'https://docs.opnsense.org/', 'https://docs.opnsense.org/')

    p = doc.add_paragraph('OPNsense Forum: ')
    add_hyperlink(p, 'https://forum.opnsense.org/', 'https://forum.opnsense.org/')

    p = doc.add_paragraph('Proxmox Dokumentation: ')
    add_hyperlink(p, 'https://pve.proxmox.com/pve-docs/', 'https://pve.proxmox.com/pve-docs/')

    # Save
    doc.save('/home/runner/work/agenten/agenten/OPNsense-auf-Proxmox-Anleitung.docx')
    print("Word-Dokument erfolgreich erstellt: OPNsense-auf-Proxmox-Anleitung.docx")

if __name__ == '__main__':
    create_word_document()
