from PyQt6.QtCore import pyqtSignal, QObject

class Signals(QObject):
    
    # Signals for the background worker
    worker_started = pyqtSignal()
    worker_paused = pyqtSignal()
    worker_resumed = pyqtSignal()
    worker_stoped = pyqtSignal()

    worker_log = pyqtSignal(str) # Used to emit logs from the background worker