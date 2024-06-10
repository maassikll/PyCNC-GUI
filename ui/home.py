# Form implementation generated from reading ui file 'home.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6.QtWidgets import QMessageBox, QFileDialog, QTableWidgetItem
from PyQt6.QtCore import QThread, QMutex, QWaitCondition
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
import cnc.main_gui as main
from ui.signals import Signals
import os
import webbrowser
from PyQt6.QtGui import QTextCursor

class GCodeExecWorker(QThread):

    _is_stoped : bool
    _is_paused : bool
    _g_code_path : str

    def __init__(self, signals : Signals, g_code_path : str):
        super().__init__()
        self.signals = signals
        self._g_code_path = g_code_path
        self._is_stoped = False
        self._is_paused = False
        self._mutex = QMutex()
        self._pause_condition = QWaitCondition()

    def run(self):
        # emit started signal
        self.signals.worker_started.emit()

        # read file with gcode from the selected path
        with open(self._g_code_path, 'r') as f:
            for line in f:

                # pause and resume logic 
                self._mutex.lock()
                if self._is_paused:
                    self._pause_condition.wait(self._mutex)
                self._mutex.unlock()

                # stop when _is_stoped is true
                if self._is_stoped:
                    break

                # decode the input and send log to the ui 
                line = line.strip()
                self.signals.worker_log.emit('> ' + line)
                
                # stop execution when there is an error
                if not main.do_line(line):
                    break

        # emit stoped signal
        self.signals.worker_stoped.emit()
            
    def pause(self):
        self.signals.worker_paused.emit()
        self._mutex.lock()
        self._is_paused = True
        self._mutex.unlock()

    def resume(self):
        self.signals.worker_resumed.emit()
        self._mutex.lock()
        self._is_paused = False
        self._mutex.unlock()
        self._pause_condition.wakeAll()
        
    def stop(self):
        self._is_stoped = True


class Ui_MainWindow(QMainWindow):

    signals : Signals
    g_code_exec : GCodeExecWorker

    def __init__(self):
        super().__init__()
        self.g_code_exec = None
        self.signals = Signals()
        
        self.setupUi(self)
        self.retranslateUi(self)
        self.setupBack()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 514)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 100))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_zenbreak = QtWidgets.QPushButton(parent=self.widget)
        self.btn_zenbreak.setEnabled(True)
        self.btn_zenbreak.setMinimumSize(QtCore.QSize(0, 90))
        self.btn_zenbreak.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btn_zenbreak.setIcon(icon)
        self.btn_zenbreak.setIconSize(QtCore.QSize(250, 200))
        self.btn_zenbreak.setFlat(True)
        self.btn_zenbreak.setObjectName("btn_zenbreak")
        self.verticalLayout_2.addWidget(self.btn_zenbreak)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.widget_2)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_path = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.file_path.setObjectName("file_path")
        self.horizontalLayout.addWidget(self.file_path)
        self.btn_path = QtWidgets.QToolButton(parent=self.groupBox_2)
        self.btn_path.setObjectName("btn_path")
        self.horizontalLayout.addWidget(self.btn_path)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.widget_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_start = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btn_start.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/images/Play.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btn_start.setIcon(icon1)
        self.btn_start.setIconSize(QtCore.QSize(48, 36))
        self.btn_start.setObjectName("btn_start")
        self.horizontalLayout_3.addWidget(self.btn_start)
        self.btn_pause = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btn_pause.setEnabled(False)
        self.btn_pause.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/images/Pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btn_pause.setIcon(icon2)
        self.btn_pause.setIconSize(QtCore.QSize(48, 36))
        self.btn_pause.setObjectName("btn_pause")
        self.horizontalLayout_3.addWidget(self.btn_pause)
        self.btn_stop = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/images/Stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.btn_stop.setIcon(icon3)
        self.btn_stop.setIconSize(QtCore.QSize(48, 36))
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout_3.addWidget(self.btn_stop)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.verticalLayout_7.addWidget(self.groupBox_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(parent=self.widget_2)
        self.groupBox.setMinimumSize(QtCore.QSize(150, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 131, 40))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=self.widget_2)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.log_textarea = QtWidgets.QPlainTextEdit(parent=self.groupBox_4)
        self.log_textarea.setObjectName("log_textarea")
        self.log_textarea.setReadOnly(True) 
        self.verticalLayout_5.addWidget(self.log_textarea)
        self.horizontalLayout_2.addWidget(self.groupBox_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyCNC GUI V1.0"))
        self.groupBox_2.setTitle(_translate("MainWindow", "G-code"))
        self.label.setText(_translate("MainWindow", "chemin G-code :"))
        self.btn_path.setText(_translate("MainWindow", "..."))
        self.groupBox_3.setTitle(_translate("MainWindow", "Commande"))
        self.groupBox.setTitle(_translate("MainWindow", "Collaborateurs"))
        self.label_2.setText(_translate("MainWindow", "Yahia Mouhemed"))
        self.label_3.setText(_translate("MainWindow", "Yahia Yassin"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Logs"))

    def setupBack(self): # setup the backend (events and connctions)
        # list of signals and their events
        signals_events = {
            self.signals.worker_started : self.workerStarted,
            self.signals.worker_paused : self.workerPaused,
            self.signals.worker_resumed : self.workerResumed,
            self.signals.worker_stoped : self.workerStoped,
            self.signals.worker_log : self.workerLog,
        }

        # connect evrey signal to is event 
        for signal, event in signals_events.items():
            signal.connect(event)

        # list of all buttons and their actions
        buttons_actions = {
            self.btn_zenbreak : self.btnZenbreak,
            self.btn_path : self.btnPath,
            self.btn_start : self.btnStart,
            self.btn_stop : self.btnStop,
            self.btn_pause : self.btnPause,
        }

        # connect all button to thier methodes 
        for button, action in buttons_actions.items():
            button.clicked.connect(action)

    def workerStarted(self):
        # clear old data
        self.log_textarea.clear()

        # disabled
        self.btn_start.setEnabled(False)
        self.file_path.setEnabled(False)
        self.btn_path.setEnabled(False)

        # enabled
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

    def workerStoped(self):
        # Enabled
        self.btn_start.setEnabled(True)
        self.file_path.setEnabled(True)
        self.btn_path.setEnabled(True)

        # Disabled
        self.btn_pause.setEnabled(False)
        self.btn_stop.setEnabled(False)

        # Other
        self.g_code_exec = None # reset worker when it is stoped
        self.info_dialog("Travail terminé.")

    def workerPaused(self):
        # Disabled
        self.btn_pause.setEnabled(False)
        self.file_path.setEnabled(False)
        self.btn_path.setEnabled(False)
        self.info_dialog("Travail pauser.")

        # Enabled
        self.btn_stop.setEnabled(True)
        self.btn_start.setEnabled(True)

    def workerResumed(self):
        # Disabled
        self.btn_start.setEnabled(False)
        self.file_path.setEnabled(False)
        self.btn_path.setEnabled(False)

        # Enabled
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

    def workerLog(self, log : str): # append log to text area
        self.log_textarea.appendPlainText(log)
        self.scrollToBottom()

    def btnZenbreak(self): # open a browser and go to github link
        url = "https://github.com/MRxACR/PyCNC-GUI"
        webbrowser.open(url)

    def btnPath(self): # show select file dialoge
        options = QFileDialog.Option.ReadOnly
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file:
            self.file_path.setText(file)

    def btnStart(self): # start or resume the worker
        if self.g_code_exec == None: # g_code_worker is in stop mode
            # get the selected path
            path = self.file_path.text()

            # check if path exists
            if not os.path.exists(path):
                self.alerte_dialog("fichier introuvable !")
                return

            self.g_code_exec = GCodeExecWorker(self.signals, path)

            # start the worker
            self.g_code_exec.start()

        else: # g_code_worker is in pause mode
            # resume the worker
            self.g_code_exec.resume()

    def btnStop(self): # stop the worker
        # check if there is g_code_exec instence to stop
        if self.g_code_exec == None:
            return
        
        # stop the worker
        self.g_code_exec.stop()

    def btnPause(self): # pause the worekr
        # check if there is g_code_exec instence to pause
        if self.g_code_exec == None:
            return
        
        # pause the worker
        self.g_code_exec.stop()

    # other functions
    def error_dialog(self, message : str):
        QMessageBox.critical(
            self,
            'Erreur',
            message,
            QMessageBox.StandardButton.Ok
        )

    def info_dialog(self, message : str):
        QMessageBox.information(
            self,
            'Information',
            message,
            QMessageBox.StandardButton.Ok
        )
    
    def alerte_dialog(self, message : str):
        QMessageBox.warning(
            self,
            'Alerte',
            message,
            QMessageBox.StandardButton.Ok
        )

    def scrollToBottom(self):
        cursor = self.log_textarea.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_textarea.setTextCursor(cursor)
        self.log_textarea.ensureCursorVisible()