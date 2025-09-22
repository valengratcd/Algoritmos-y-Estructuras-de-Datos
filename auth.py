from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt, Signal

class AuthWidget(QWidget):
    logged_in = Signal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init()

    def init(self):
        l = QVBoxLayout(self)
        t = QLabel("PlayStore Sim - Autenticación")
        t.setAlignment(Qt.AlignCenter)
        l.addWidget(t)

        f = QFormLayout()
        self.user = QLineEdit()
        self.passw = QLineEdit()
        self.passw.setEchoMode(QLineEdit.Password)
        f.addRow("Usuario", self.user)
        f.addRow("Password", self.passw)
        l.addLayout(f)

        h = QHBoxLayout()
        breg = QPushButton("Registrarse")
        blog = QPushButton("Iniciar sesión")
        breg.clicked.connect(self.register)
        blog.clicked.connect(self.login)
        h.addWidget(breg); h.addWidget(blog)
        l.addLayout(h)

    def register(self):
        u, p = self.user.text().strip(), self.passw.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "Error", "Usuario y password requeridos")
            return
        ok, msg = self.db.create_user(u, p)
        if ok:
            QMessageBox.information(self, "Registro", "Usuario creado")
        else:
            QMessageBox.warning(self, "Error", f"No se pudo crear: {msg}")

    def login(self):
        u, p = self.user.text().strip(), self.passw.text().strip()
        if self.db.check_user(u, p):
            self.logged_in.emit()
        else:
            QMessageBox.warning(self, "Error", "Credenciales inválidas")
