from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QListWidget, QListWidgetItem, QProgressBar, QCheckBox, QMessageBox,
    QSpinBox
)
from PySide6.QtCore import Qt, QTimer
from downloads import DownloadThread
import threading


class StoreWidget(QWidget):
    """
    Interfaz de la tienda de aplicaciones vinculada a un teléfono.
    Permite descargar apps, ver instaladas y simular compras.
    """

    def __init__(self, db):
        super().__init__()
        self.db = db

        # Variables de control
        self.download_thread = None
        self.cancel_event = None
        self.internet = True
        self.apps = []
        self.phones = []

        # Inicializar interfaz y datos
        self.init_ui()
        self.load_data()

    # ==============================================================
    # Configuración de interfaz
    # ==============================================================

    def init_ui(self):
        """Construye toda la interfaz gráfica."""
        main_layout = QVBoxLayout(self)

        # --- Sección superior (selección de teléfono y wifi)
        top_layout = QHBoxLayout()

        self.phone_select = QComboBox()
        self.refresh_phones_btn = QPushButton("Refrescar")

        top_layout.addWidget(QLabel("Teléfono:"))
        top_layout.addWidget(self.phone_select)
        top_layout.addWidget(self.refresh_phones_btn)

        self.internet_chk = QCheckBox("WiFi conectado")
        self.internet_chk.setChecked(True)
        top_layout.addWidget(self.internet_chk)

        main_layout.addLayout(top_layout)

        # --- Cuerpo (catálogo a la izquierda / detalles a la derecha)
        body_layout = QHBoxLayout()

        # Catálogo
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Catálogo"))

        self.catalog_list = QListWidget()
        left_layout.addWidget(self.catalog_list)

        catalog_buttons = QHBoxLayout()
        self.download_btn = QPushButton("Descargar/Comprar")
        self.info_btn = QPushButton("Info")
        catalog_buttons.addWidget(self.download_btn)
        catalog_buttons.addWidget(self.info_btn)

        left_layout.addLayout(catalog_buttons)
        body_layout.addLayout(left_layout, 60)

        # Detalles del teléfono
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Teléfono - Detalles"))

        self.details_label = QLabel("")
        self.details_label.setWordWrap(True)
        right_layout.addWidget(self.details_label)

        right_layout.addWidget(QLabel("Instaladas"))
        self.installed_list = QListWidget()
        right_layout.addWidget(self.installed_list)

        self.progress = QProgressBar()
        right_layout.addWidget(self.progress)

        body_layout.addLayout(right_layout, 40)
        main_layout.addLayout(body_layout)

        # --- Inferior (controles de velocidad y notificaciones)
        bottom_layout = QHBoxLayout()

        self.notify_btn = QPushButton("Ver notificaciones")
        self.time_spin = QSpinBox()
        self.time_spin.setRange(1, 120)
        self.time_spin.setValue(5)

        bottom_layout.addWidget(QLabel("Velocidad (KB/s)"))
        bottom_layout.addWidget(self.time_spin)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.notify_btn)

        main_layout.addLayout(bottom_layout)

        # --- Conexiones de eventos
        self.refresh_phones_btn.clicked.connect(self.load_phones)
        self.phone_select.currentIndexChanged.connect(self.on_phone_change)
        self.catalog_list.itemDoubleClicked.connect(self.on_catalog_double)
        self.download_btn.clicked.connect(self.on_download_click)
        self.info_btn.clicked.connect(self.on_info_click)
        self.notify_btn.clicked.connect(self.show_notification)
        self.internet_chk.stateChanged.connect(self.on_internet_toggle)

        # --- Temporizador de notificaciones
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_upcoming)
        self.timer.start(10000)

    # ==============================================================
    # Carga de datos
    # ==============================================================

    def load_data(self):
        self.load_phones()
        self.load_catalog()

    def load_phones(self):
        """Carga la lista de teléfonos desde la base de datos."""
        self.phone_select.clear()
        self.phones = []

        for phone in self.db.get_phones():
            phone_dict = {
                "id": phone[0],
                "name": phone[1],
                "storage_total": phone[2],
                "storage_used": phone[3],
                "version": phone[4],
            }
            self.phones.append(phone_dict)
            self.phone_select.addItem(phone_dict["name"], phone_dict)

        if self.phones:
            self.update_phone_view(self.phones[0])

    def load_catalog(self):
        """Carga el catálogo de apps desde la base de datos."""
        self.catalog_list.clear()
        self.apps = []

        for app in self.db.get_apps():
            app_dict = {
                "id": app[0],
                "name": app[1],
                "size": app[2],
                "min_version": app[3],
                "price": app[4],
                "is_paid": bool(app[5]),
            }
            self.apps.append(app_dict)

            item_text = (
                f"{app_dict['name']} - {app_dict['size'] // 1024}MB "
                f"- v{app_dict['min_version']}"
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, app_dict)
            self.catalog_list.addItem(item)

    # ==============================================================
    # Manejo de selección de teléfono
    # ==============================================================

    def on_phone_change(self, index):
        data = self.phone_select.currentData()
        if data:
            self.update_phone_view(data)

    def update_phone_view(self, phone):
        """Muestra la información del teléfono seleccionado."""
        free = phone["storage_total"] - phone["storage_used"]
        details = (
            f"{phone['name']}\n"
            f"Total: {phone['storage_total'] // 1024}MB\n"
            f"Usado: {phone['storage_used'] // 1024}MB\n"
            f"Libre: {free // 1024}MB\n"
            f"Versión: {phone['version']}"
        )
        self.details_label.setText(details)

        self.installed_list.clear()
        for installed in self.db.get_installed(phone["id"]):
            self.installed_list.addItem(
                f"{installed[1]} - {installed[2] // 1024}MB"
            )

    # ==============================================================
    # Catálogo
    # ==============================================================

    def on_catalog_double(self, item):
        self.catalog_list.setCurrentItem(item)
        self.on_info_click()

    def on_info_click(self):
        """Muestra la información detallada de la app seleccionada."""
        item = self.catalog_list.currentItem()
        if not item:
            return

        app = item.data(Qt.UserRole)
        message = (
            f"{app['name']}\n"
            f"Tamaño: {app['size'] // 1024}MB\n"
            f"Min ver: {app['min_version']}\n"
            f"Precio: {'$' + str(app['price']) if app['is_paid'] else 'Gratis'}"
        )
        QMessageBox.information(self, "Info app", message)

    # ==============================================================
    # Descargas
    # ==============================================================

    def on_internet_toggle(self, state):
        self.internet = self.internet_chk.isChecked()

    def on_download_click(self):
        """Inicia la descarga de la app seleccionada."""
        item = self.catalog_list.currentItem()
        if not item:
            return

        app = item.data(Qt.UserRole)
        phone = self.phone_select.currentData()

        # Validaciones
        if not self.internet:
            QMessageBox.warning(self, "Error",
                                "No hay WiFi. No se puede descargar.")
            return

        if self.db.is_installed(phone["id"], app["id"]):
            QMessageBox.information(self, "Info", "App ya instalada.")
            return

        free = phone["storage_total"] - phone["storage_used"]
        if app["min_version"] > phone["version"] or app["size"] > free:
            QMessageBox.warning(self, "Incompatible",
                                "El celular no soporta la app o "
                                "no tiene espacio suficiente.")
            return

        if app["is_paid"]:
            confirm = QMessageBox.question(
                self,
                "Compra",
                f"Pagar ${app['price']} por {app['name']}?"
            )
            if confirm != QMessageBox.Yes:
                return

        # Configurar barra de progreso y descarga
        self.progress.setValue(0)
        speed = self.time_spin.value() * 1024
        self.cancel_event = threading.Event()

        self.download_thread = DownloadThread(
            app, phone, self.db, speed,
            self.on_progress, self.on_finish, self.cancel_event
        )
        self.download_thread.start()

    def on_progress(self, percent):
        """Actualiza la barra de progreso en el hilo principal."""
        QTimer.singleShot(0, lambda: self.progress.setValue(percent))

    def on_finish(self):
        QTimer.singleShot(0, self.finish_ui)

    def finish_ui(self):
        QMessageBox.information(self, "OK",
                                "Descarga e instalación completadas.")
        self.load_phones()
        self.load_catalog()

    def show_notification(self):
        for app in self.apps:
            if app["name"] == "UpcomingBattle":
                QMessageBox.information(
                    self,
                    "Notificación",
                    "Próximo juego en lanzamiento: UpcomingBattle"
                )
                return
        QMessageBox.information(self, "Notificación",
                                "Sin nuevas notificaciones.")

    def check_upcoming(self):
        for app in self.apps:
            if app["name"] == "UpcomingBattle":
                pass  # Simulación: se podría agregar lógica extra
