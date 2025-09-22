"""
downloads.py

Módulo que contiene la clase DownloadThread para simular
descargas de aplicaciones en segundo plano.
"""

import threading
import time
from typing import Callable, Dict, Optional


class DownloadThread(threading.Thread):
    """
    Hilo que simula la descarga de una aplicación.

    Parámetros:
    - app: dict con los campos mínimos 'id' y 'size' (size en KB).
    - phone: dict con los campos mínimos 'id' y 'storage_used'.
    - db: instancia del módulo database.DB con métodos update_phone_used
      y add_install.
    - speed_kb_s: velocidad en KB/s (entero).
    - progress_callback: Callable[[int], None] para recibir % de avance.
    - finish_callback: Callable[[], None] para notificar finalización.
    - cancel_event: threading.Event opcional para cancelar la descarga.
    """

    def __init__(
        self,
        app: Dict,
        phone: Dict,
        db,
        speed_kb_s: int,
        progress_callback: Callable[[int], None],
        finish_callback: Callable[[], None],
        cancel_event: Optional[threading.Event] = None,
    ) -> None:
        super().__init__(daemon=True)
        self.app = app
        self.phone = phone
        self.db = db
        self.speed_kb_s = max(1, int(speed_kb_s))
        self.progress_callback = progress_callback
        self.finish_callback = finish_callback
        self.cancel_event = cancel_event or threading.Event()

    def run(self) -> None:
        size_kb = int(self.app.get("size", 0))
        total_seconds = max(1, int(size_kb / (self.speed_kb_s + 1)))

        try:
            for second in range(total_seconds + 1):
                if self.cancel_event.is_set():
                    return

                percent = int(second * 100 / total_seconds)
                try:
                    self.progress_callback(percent)
                except Exception:
                    # Ignorar errores en el callback para no romper el hilo
                    pass

                time.sleep(1)

            if self.cancel_event.is_set():
                return

            new_used = int(self.phone.get("storage_used", 0)) + size_kb

            try:
                self.db.update_phone_used(self.phone["id"], new_used)
                self.db.add_install(self.phone["id"], self.app["id"])
            except Exception:
                # Si falla el guardado en la BD, terminamos silenciosamente
                pass

            try:
                self.finish_callback()
            except Exception:
                pass

        except Exception:
            return

    def cancel(self) -> None:
        """Solicita la cancelación de la descarga."""
        self.cancel_event.set()
