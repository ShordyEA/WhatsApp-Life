import sys
import time
import random
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QProgressBar, QFrame, QGraphicsDropShadowEffect,
                             QScrollArea, QMessageBox, QFileDialog,
                             QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, 
                             QAbstractItemView, QComboBox, QInputDialog, QDialog,
                             QStackedWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QUrl
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap, QPainter, QPainterPath

# -----------------------------------------------------------------------------
# IMPORTACIONES EXTERNAS (Selenium removido para proteger el código fuente)
# -----------------------------------------------------------------------------
try:
    import openpyxl
except ImportError:
    print("ERROR CRÍTICO: Biblioteca OpenPyXL no encontrada.")
    print("Por favor, ejecuta: pip install openpyxl")

# -----------------------------------------------------------------------------
# CONFIGURACIONES GLOBALES Y RUTAS
# -----------------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_NAME = "LyCodelife"
ROAMING_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
DB_FILE = os.path.join(ROAMING_DIR, "contacts.xlsx")
LISTS_FILE = os.path.join(ROAMING_DIR, "lists.json")
BACKUP_DIR = os.path.join(ROAMING_DIR, "backups")
CONFIG_FILE = os.path.join(ROAMING_DIR, "config.json")

LOGO_PATH = os.path.join(os.path.expanduser("~"), "Documents", "LyCodelife", "logo.jpeg")
ICON_PATH = os.path.join(BASE_DIR, "whatsly.ico")

if not os.path.exists(ROAMING_DIR):
    os.makedirs(ROAMING_DIR)
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# -----------------------------------------------------------------------------
# ESTILOS (QSS) - MANTENIDOS IDÉNTICOS PARA LA PRESENTACIÓN
# -----------------------------------------------------------------------------
STYLESHEET = """
QMainWindow {
    background-color: #09090b;
}
QWidget {
    font-family: 'Segoe UI', sans-serif;
    color: #e4e4e7;
}
QFrame.Card {
    background-color: #18181b;
    border-radius: 16px;
    border: 1px solid #27272a;
}
QFrame.Card:hover {
    border: 1px solid #10b981;
    background-color: #202025;
}
QPushButton.PrimaryButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10b981, stop:1 #059669);
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    font-size: 14px;
    border: none;
}
QPushButton.PrimaryButton:hover {
    background-color: #34d399;
}
QPushButton.DangerButton {
    background-color: #ef4444;
    color: white;
    border-radius: 12px;
    padding: 8px;
    font-weight: bold;
    border: none;
}
QPushButton.DangerButton:hover {
    background-color: #f87171;
}
QPushButton.GhostButton {
    background-color: transparent;
    border: 1px solid #3f3f46;
    color: #a1a1aa;
    border-radius: 12px;
    padding: 8px;
}
QPushButton.GhostButton:hover {
    border: 1px solid #10b981;
    color: #10b981;
    background-color: rgba(16, 185, 129, 0.1);
}
QPushButton#AttachButton {
    background-color: #27272a;
    border: 1px dashed #52525b;
    color: #a1a1aa;
    text-align: left;
    padding-left: 15px;
    border-radius: 10px;
}
QPushButton#AttachButton:hover {
    border: 1px dashed #10b981;
    color: #10b981;
    background-color: #202025;
}
QPushButton.StepButton {
    background-color: #27272a;
    color: #a1a1aa;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
}
QPushButton.StepButton:checked {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid #10b981;
}
QLineEdit, QTextEdit, QComboBox {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 10px;
    padding: 10px;
    color: #ffffff;
    font-size: 13px;
    selection-background-color: #10b981;
    selection-color: white;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #10b981;
}
QTableWidget {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 12px;
    gridline-color: #27272a;
    color: #e4e4e7;
    selection-background-color: #10b981;
    selection-color: white;
}
QHeaderView::section {
    background-color: #27272a;
    padding: 8px;
    border: none;
    font-weight: bold;
    color: #a1a1aa;
}
QScrollBar:vertical {
    background: #09090b;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #3f3f46;
    border-radius: 4px;
}
QLabel.Title {
    font-size: 24px;
    font-weight: 800;
    color: white;
}
QLabel.Subtitle {
    font-size: 13px;
    color: #71717a;
}
QLabel.StatValue {
    font-size: 36px;
    font-weight: 300;
    color: #10b981;
}
QLabel.StatLabel {
    font-size: 11px;
    font-weight: bold;
    color: #52525b;
}
QFrame.SideMenu {
    background-color: #18181b;
    border-right: 1px solid #27272a;
}
QPushButton.MenuButton {
    text-align: left;
    padding: 15px 20px;
    background-color: transparent;
    color: #a1a1aa;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
}
QPushButton.MenuButton:checked {
    background-color: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border-right: 3px solid #10b981;
}
"""

class ImagePreviewDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vista Previa")
        self.setModal(True)
        self.resize(800, 600)
        self.setStyleSheet("background-color: #09090b;")
        layout = QVBoxLayout(self)
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaled(780, 580, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            label.setText("No se pudo cargar la imagen")
            label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(label)
        btn_close = QPushButton("Cerrar Vista Previa")
        btn_close.setStyleSheet("background-color: #27272a; color: white; padding: 12px; border-radius: 8px;")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

class AttachmentThumbnail(QFrame):
    delete_clicked = pyqtSignal(str)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setFixedSize(70, 70)
        self.setStyleSheet("background: #27272a; border-radius: 8px; border: 1px solid #3f3f46;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        lbl_img = QLabel()
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
            pix = QPixmap(file_path)
            if not pix.isNull():
                lbl_img.setPixmap(pix.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            else:
                lbl_img.setText("IMG")
        else:
            lbl_img.setText("FILE")
            lbl_img.setStyleSheet("color: #a1a1aa; font-weight: bold; font-size: 10px; border:none;")
        layout.addWidget(lbl_img)
        self.btn_del = QPushButton("×", self)
        self.btn_del.setFixedSize(20, 20)
        self.btn_del.move(50, 0)
        self.btn_del.setStyleSheet("background: #ef4444; color: white; border-radius: 10px; border: none;")
        self.btn_del.clicked.connect(self.on_delete)
        
    def on_delete(self):
        self.delete_clicked.emit(self.file_path)

class NeonStatCard(QFrame):
    def __init__(self, title, value, icon="📊", color="#10b981"):
        super().__init__()
        self.setProperty("class", "Card")
        self.setFixedHeight(120)
        layout = QVBoxLayout(self)
        header = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 20px; color: {color};")
        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "StatLabel")
        header.addWidget(icon_lbl)
        header.addWidget(title_lbl)
        header.addStretch()
        self.value_lbl = QLabel(value)
        self.value_lbl.setProperty("class", "StatValue")
        self.value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_lbl.setStyleSheet(f"color: {color};")
        layout.addLayout(header)
        layout.addWidget(self.value_lbl)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        col = QColor(color)
        col.setAlpha(60) 
        shadow.setColor(col)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def update_value(self, val):
        self.value_lbl.setText(str(val))

# -----------------------------------------------------------------------------
# WORKER SIMULADO (La lógica principal fue removida y reemplazada por simulaciones)
# -----------------------------------------------------------------------------
class BotWorker(QThread):
    log_signal = pyqtSignal(str, str) 
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()
    status_signal = pyqtSignal(bool)
    save_driver_signal = pyqtSignal(str)
    count_update_signal = pyqtSignal(int, int)
    copy_signal = pyqtSignal(list)
    
    def __init__(self, contacts, campaign_steps, chrome_path, cached_driver_path=None):
        super().__init__()
        self.contacts = contacts 
        self.campaign_steps = campaign_steps
        self.is_running = True
        self.stats = {'sent': 0, 'invalid': 0, 'failed': 0, 'start_time': None}

    def run(self):
        total = len(self.contacts)
        self.stats['start_time'] = time.time()
        self.status_signal.emit(True) 
        step_count = len(self.campaign_steps)
        self.log_signal.emit(f"🚀 Iniciando motor (MODO DEMO): {total} contactos, {step_count} mensajes en cadena.", "system")

        try:
            # Simular carga de Chrome
            self.log_signal.emit("🔍 Preparando entorno seguro...", "info")
            time.sleep(1)
            self.log_signal.emit("🌍 Abriendo WhatsApp Web...", "system")
            time.sleep(2)
            self.log_signal.emit("🔓 Sesión iniciada correctamente.", "success")
            time.sleep(1)
            
            for i, contact in enumerate(self.contacts):
                if not self.is_running: break
                name = contact['name']
                display_name = name if name else ""
                
                self.log_signal.emit(f"🔄 Contacto {i+1}/{total}: <b>{name}</b>", "info")
                time_start = time.time()
                
                # Simular apertura de chat
                time.sleep(1.5)

                for step_idx, step in enumerate(self.campaign_steps):
                    if not self.is_running: break
                    step_text = step.get('text', '').replace("nombre", display_name)
                    step_files = step.get('attachments', [])
                    
                    self.log_signal.emit(f"  ➜ Enviando Mensaje {step_idx + 1}...", "typing")
                    time.sleep(1)
                    
                    if step_text:
                        time.sleep(random.uniform(0.5, 1.0))
                    
                    if step_files:
                        self.log_signal.emit(f"  📎 Adjuntando {len(step_files)} archivos...", "typing")
                        time.sleep(1.5)
                        self.log_signal.emit("  ✅ Archivos enviados.", "success")
                    
                    if step_idx < len(self.campaign_steps) - 1:
                        time.sleep(random.uniform(1, 2))

                duration = time.time() - time_start
                self.log_signal.emit(f"✅ Secuencia terminada ({duration:.1f}s)", "success")
                self.stats['sent'] += 1
                self.count_update_signal.emit(1, 0)
                self.progress_signal.emit(int(((i+1)/total)*100))
                time.sleep(1.5)

        except Exception as e:
            self.log_signal.emit(f"🔥 Error Crítico: {str(e)}", "error")
        finally:
            self.status_signal.emit(False)
            total_time = time.time() - (self.stats['start_time'] or time.time())
            mins, secs = divmod(total_time, 60)
            report = f"""
            <br>
            <div style="border:1px solid #10b981; padding:10px; border-radius:10px; background-color: #18181b;">
                <b style="color:#10b981; font-size: 14px;">🏁 CAMPAÑA FINALIZADA (DEMO)</b><br><br>
                ⏱️ Tiempo: <b>{int(mins)}m {int(secs)}s</b><br>
                ✅ Contactos Completados: <b style="color:#10b981;">{self.stats['sent']}</b><br>
                🚫 Inválidos: <b style="color:#f59e0b;">{self.stats['invalid']}</b><br>
                ❌ Fallidos: <b style="color:#ef4444;">{self.stats['failed']}</b>
            </div>
            """
            self.log_signal.emit(report, "system")
            self.finished_signal.emit()

    def stop(self):
        self.is_running = False

# -----------------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LyCodeLife WhatsApp Automatización - MODO PRESENTACIÓN")
        self.resize(1280, 850)
        self.setStyleSheet(STYLESHEET)
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        
        self.config = {}
        self.contacts_data = []
        self.saved_lists = {}
        self.active_contacts_count = 0 
        self.campaign_steps = [{'text': "", 'attachments': []}]
        self.current_step_index = 0

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setProperty("class", "SideMenu")
        sidebar.setFixedWidth(260)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(15, 30, 15, 30)
        
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(100, 100)
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo.setText("LY")
        self.lbl_logo.setStyleSheet("background-color: #27272a; color: #10b981; font-weight: bold; border-radius: 50px; font-size: 24px;")
        
        logo_container = QHBoxLayout()
        logo_container.addWidget(self.lbl_logo)
        side_layout.addLayout(logo_container)
        
        lbl_brand = QLabel("LyCodelife")
        lbl_brand.setProperty("class", "Title")
        lbl_brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(lbl_brand)
        
        lbl_sub = QLabel("Automatización PRO (Demo)")
        lbl_sub.setProperty("class", "Subtitle")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(lbl_sub)
        side_layout.addSpacing(30)

        self.btn_menu_home = QPushButton("  Panel Principal")
        self.btn_menu_home.setProperty("class", "MenuButton")
        self.btn_menu_home.setCheckable(True)
        self.btn_menu_home.setChecked(True)
        self.btn_menu_home.clicked.connect(lambda: self.switch_page(0))
        
        self.btn_menu_contacts = QPushButton("  Gestor Contactos")
        self.btn_menu_contacts.setProperty("class", "MenuButton")
        self.btn_menu_contacts.setCheckable(True)
        self.btn_menu_contacts.clicked.connect(lambda: self.switch_page(1))

        side_layout.addWidget(self.btn_menu_home)
        side_layout.addWidget(self.btn_menu_contacts)
        side_layout.addStretch()
        main_layout.addWidget(sidebar)

        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)

        top_bar = QHBoxLayout()
        self.lbl_page_title = QLabel("Panel de Control")
        self.lbl_page_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        
        self.status_widget = QFrame()
        self.status_widget.setFixedSize(140, 36)
        self.status_widget.setStyleSheet("background-color: #18181b; border-radius: 18px; border: 1px solid #27272a;")
        stat_layout = QHBoxLayout(self.status_widget)
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #ef4444; font-size: 14px;")
        self.status_text = QLabel("OFFLINE")
        self.status_text.setStyleSheet("color: #71717a; font-weight: bold; font-size: 11px;")
        stat_layout.addWidget(self.status_indicator)
        stat_layout.addWidget(self.status_text)
        
        top_bar.addWidget(self.lbl_page_title)
        top_bar.addStretch()
        top_bar.addWidget(self.status_widget)
        content_layout.addLayout(top_bar)

        self.stack = QStackedWidget()
        
        # PÁGINA 1: DASHBOARD
        page_home = QWidget()
        home_layout = QVBoxLayout(page_home)
        
        cards_layout = QHBoxLayout()
        self.card_sent = NeonStatCard("ENVIADOS", "0", "📨", "#10b981")
        self.card_pending = NeonStatCard("PENDIENTES", "0", "⏳", "#f59e0b")
        self.card_failed = NeonStatCard("FALLIDOS", "0", "✖", "#ef4444")
        cards_layout.addWidget(self.card_sent)
        cards_layout.addWidget(self.card_pending)
        cards_layout.addWidget(self.card_failed)
        home_layout.addLayout(cards_layout)

        split_layout = QHBoxLayout()
        msg_frame = QFrame()
        msg_frame.setProperty("class", "Card")
        msg_layout = QVBoxLayout(msg_frame)
        
        hud_layout = QHBoxLayout()
        self.cb_dashboard_lists = QComboBox()
        self.cb_dashboard_lists.addItem("Cargar Plantilla de Contactos...")
        hud_layout.addWidget(QLabel("👥 Destinatarios:"))
        hud_layout.addWidget(self.cb_dashboard_lists)
        msg_layout.addLayout(hud_layout)
        
        self.steps_bar = QScrollArea()
        self.steps_bar.setFixedHeight(50)
        self.steps_bar.setWidgetResizable(True)
        self.steps_bar.setStyleSheet("background: transparent; border: none;")
        self.steps_container = QWidget()
        self.steps_layout = QHBoxLayout(self.steps_container)
        self.steps_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.steps_bar.setWidget(self.steps_container)
        msg_layout.addWidget(self.steps_bar)
        
        self.txt_message = QTextEdit()
        self.txt_message.setPlaceholderText("Escribe el mensaje para este paso...")
        self.txt_message.textChanged.connect(self.save_current_step_text)
        msg_layout.addWidget(self.txt_message)
        
        att_layout = QHBoxLayout()
        self.btn_attach = QPushButton("  Adjuntar (+)")
        self.btn_attach.setObjectName("AttachButton")
        self.btn_attach.setFixedSize(130, 45)
        self.btn_attach.clicked.connect(self.select_attachment)
        self.scroll_attachments = QScrollArea()
        self.scroll_attachments.setFixedHeight(80)
        self.scroll_attachments.setWidgetResizable(True)
        self.scroll_attachments.setStyleSheet("background: transparent; border: none;")
        self.thumbs_container = QWidget()
        self.thumbs_layout = QHBoxLayout(self.thumbs_container)
        self.thumbs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.scroll_attachments.setWidget(self.thumbs_container)
        att_layout.addWidget(self.btn_attach)
        att_layout.addWidget(self.scroll_attachments)
        msg_layout.addLayout(att_layout)
        
        act_layout = QHBoxLayout()
        self.btn_start = QPushButton("INICIAR CAMPAÑA")
        self.btn_start.setProperty("class", "PrimaryButton")
        self.btn_start.clicked.connect(self.start_bot)
        self.btn_stop = QPushButton("DETENER")
        self.btn_stop.setProperty("class", "DangerButton")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_bot)
        act_layout.addWidget(self.btn_start)
        act_layout.addWidget(self.btn_stop)
        msg_layout.addLayout(act_layout)

        log_frame = QFrame()
        log_frame.setProperty("class", "Card")
        log_l = QVBoxLayout(log_frame)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #09090b; border: none; font-family: 'Consolas'; font-size: 11px;")
        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("QProgressBar {background: #27272a; border-radius: 4px; height: 6px; border:none;} QProgressBar::chunk {background: #10b981; border-radius: 4px;}")
        log_l.addWidget(QLabel("REGISTRO DE SISTEMA"))
        log_l.addWidget(self.console)
        log_l.addWidget(self.pbar)

        split_layout.addWidget(msg_frame, 5)
        split_layout.addWidget(log_frame, 3)
        home_layout.addLayout(split_layout)

        # PÁGINA 2: CONTACTOS
        page_contacts = QWidget()
        cont_layout = QVBoxLayout(page_contacts)
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("🔍 Buscar por nombre o número...")
        self.inp_search.textChanged.connect(self.refresh_table)
        cont_layout.addWidget(self.inp_search)

        tools_frame = QFrame()
        tools_frame.setProperty("class", "Card")
        tools_l = QHBoxLayout(tools_frame)
        self.inp_c_name = QLineEdit()
        self.inp_c_name.setPlaceholderText("Nombre")
        self.inp_c_num = QLineEdit()
        self.inp_c_num.setPlaceholderText("Número")
        btn_c_add = QPushButton("AGREGAR")
        btn_c_add.setProperty("class", "GhostButton")
        btn_c_add.clicked.connect(self.add_manual_contact)
        btn_c_del = QPushButton("ELIMINAR")
        btn_c_del.setProperty("class", "DangerButton")
        btn_c_del.clicked.connect(self.delete_contact)
        tools_l.addWidget(self.inp_c_name)
        tools_l.addWidget(self.inp_c_num)
        tools_l.addWidget(btn_c_add)
        tools_l.addWidget(btn_c_del)
        cont_layout.addWidget(tools_frame)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["", "NOMBRE", "TELÉFONO"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        cont_layout.addWidget(self.table)

        self.stack.addWidget(page_home)
        self.stack.addWidget(page_contacts)
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_area)

        self.worker = None
        
        # Insertar contactos de prueba para demostración
        self.contacts_data = [
            {'name': 'Cliente Prueba 1', 'number': '123456789'},
            {'name': 'Cliente Prueba 2', 'number': '987654321'},
            {'name': 'Cliente Prueba 3', 'number': '555555555'}
        ]
        self.refresh_table()
        self.refresh_steps_ui()

    def refresh_steps_ui(self):
        while self.steps_layout.count():
            item = self.steps_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for i, step in enumerate(self.campaign_steps):
            btn = QPushButton(f"Mensaje {i+1}")
            btn.setProperty("class", "StepButton")
            btn.setCheckable(True)
            if i == self.current_step_index: btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=i: self.switch_step(idx))
            self.steps_layout.addWidget(btn)
        btn_add = QPushButton("+")
        btn_add.setProperty("class", "StepButton")
        btn_add.clicked.connect(self.add_step)
        self.steps_layout.addWidget(btn_add)
        self.load_step_data_to_ui()

    def load_step_data_to_ui(self):
        step = self.campaign_steps[self.current_step_index]
        self.txt_message.blockSignals(True)
        self.txt_message.setText(step['text'])
        self.txt_message.blockSignals(False)
        self.refresh_attachments_ui()

    def refresh_attachments_ui(self):
        while self.thumbs_layout.count():
            item = self.thumbs_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for fpath in self.campaign_steps[self.current_step_index]['attachments']:
            thumb = AttachmentThumbnail(fpath)
            thumb.delete_clicked.connect(self.remove_attachment)
            self.thumbs_layout.addWidget(thumb)

    def switch_step(self, index):
        self.current_step_index = index
        self.refresh_steps_ui()

    def add_step(self):
        self.campaign_steps.append({'text': "", 'attachments': []})
        self.current_step_index = len(self.campaign_steps) - 1
        self.refresh_steps_ui()

    def save_current_step_text(self):
        self.campaign_steps[self.current_step_index]['text'] = self.txt_message.toPlainText()

    def select_attachment(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar", "", "Media (*.jpg *.png *.mp4 *.pdf)")
        if files:
            for f in files:
                if f not in self.campaign_steps[self.current_step_index]['attachments']:
                    self.campaign_steps[self.current_step_index]['attachments'].append(f)
            self.refresh_attachments_ui()

    def remove_attachment(self, file_path):
        if file_path in self.campaign_steps[self.current_step_index]['attachments']:
            self.campaign_steps[self.current_step_index]['attachments'].remove(file_path)
            self.refresh_attachments_ui()

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_menu_home.setChecked(index == 0)
        self.btn_menu_contacts.setChecked(index == 1)

    def set_active_status(self, is_online):
        if is_online:
            self.status_text.setText("ONLINE")
            self.status_text.setStyleSheet("color: #10b981; font-weight: bold;")
            self.status_indicator.setStyleSheet("color: #10b981;")
        else:
            self.status_text.setText("OFFLINE")
            self.status_text.setStyleSheet("color: #71717a; font-weight: bold;")
            self.status_indicator.setStyleSheet("color: #ef4444;")

    def start_bot(self):
        if not any(step['text'].strip() or step['attachments'] for step in self.campaign_steps):
            self.log_msg("❌ Debes configurar al menos un mensaje con texto o archivo.", "error")
            return

        selected = [{'name': self.table.item(r, 1).text(), 'number': self.table.item(r, 2).text()} 
                    for r in range(self.table.rowCount()) if self.table.item(r, 0).checkState() == Qt.CheckState.Checked]
        if not selected: return

        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.active_contacts_count = len(selected)
        
        self.card_sent.update_value(0)
        self.card_failed.update_value(0)
        self.card_pending.update_value(self.active_contacts_count)

        # Usando driver_path dummy para protección
        self.worker = BotWorker(selected, self.campaign_steps, "dummy_path", None)
        self.worker.log_signal.connect(self.log_msg)
        self.worker.progress_signal.connect(self.pbar.setValue)
        self.worker.status_signal.connect(self.set_active_status)
        self.worker.finished_signal.connect(self.on_finish)
        self.worker.count_update_signal.connect(self.update_live_stats)
        self.worker.start()

    def update_live_stats(self, sent_inc, failed_inc):
        self.card_sent.update_value(int(self.card_sent.value_lbl.text()) + sent_inc)
        self.card_failed.update_value(int(self.card_failed.value_lbl.text()) + failed_inc)
        self.active_contacts_count -= (sent_inc + failed_inc)
        self.card_pending.update_value(max(0, self.active_contacts_count))

    def stop_bot(self):
        if self.worker: self.worker.stop()
        self.btn_stop.setEnabled(False)
        self.log_msg("⚠️ Deteniendo motor...", "system")

    def log_msg(self, m, t):
        c = "#a1a1aa"
        if t=="success": c="#10b981"
        elif t=="error": c="#ef4444"
        elif t=="system": c="#f59e0b"
        elif t=="typing": c="#3b82f6"
        ts = time.strftime("%H:%M:%S")
        if "div" in m: self.console.append(m)
        else: self.console.append(f'<div style="margin-bottom:2px;"><span style="color:#52525b;">{ts}</span> <b style="color:{c};">{m}</b></div>')
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

    def on_finish(self):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.set_active_status(False)
        self.pbar.setValue(100)

    def refresh_table(self):
        filter_txt = self.inp_search.text().lower().strip()
        visible_data = [(i, c) for i, c in enumerate(self.contacts_data) if filter_txt in c['name'].lower() or filter_txt in c['number']]
        self.table.setRowCount(len(visible_data))
        for i, (real_index, c) in enumerate(visible_data):
            ck = QTableWidgetItem()
            ck.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            ck.setCheckState(Qt.CheckState.Checked)
            self.table.setItem(i, 0, ck)
            self.table.setItem(i, 1, QTableWidgetItem(c['name']))
            self.table.setItem(i, 2, QTableWidgetItem(c['number']))
        self.card_pending.update_value(len(self.contacts_data))

    def add_manual_contact(self):
        n = self.inp_c_name.text().strip() or "Cliente"
        m = self.inp_c_num.text().strip()
        if m and not any(d['number'] == m for d in self.contacts_data):
            self.contacts_data.append({'name': n, 'number': m})
            self.refresh_table()
            self.inp_c_name.clear()
            self.inp_c_num.clear()

    def delete_contact(self):
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        if selected_rows:
            for row in selected_rows: del self.contacts_data[row]
            self.refresh_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
