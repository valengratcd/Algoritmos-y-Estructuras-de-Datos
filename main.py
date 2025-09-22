import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database import DB
from auth import AuthWidget
from store import StoreWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.setWindowTitle("PlayStore Sim")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.auth = AuthWidget(self.db)
        self.store = StoreWidget(self.db)

        self.stack.addWidget(self.auth)
        self.stack.addWidget(self.store)

        self.auth.logged_in.connect(self.enter_store)

    def enter_store(self):
        self.stack.setCurrentWidget(self.store)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    w.show()
    sys.exit(app.exec())
