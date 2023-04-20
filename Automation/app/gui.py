from multiprocessing import Pipe, Process, freeze_support
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, QThread
from .ui.appgui import Ui_MainWindow
from .automation import main_caller

freeze_support()

class Thread(QThread):
    log = pyqtSignal(str)

    def __init__(self,parent=None):
        super(Thread, self).__init__(parent)

    def run(self):
        scraper = "log_file.log"
        try:
            fp = open(scraper,"r")
        except FileNotFoundError:
            time.sleep(10)
            fp = open(scraper,"r")
        while 1:
            where = fp.tell()
            line = fp.readline()
            if not line:
                time.sleep(2)
                fp.seek(where)
            else:
                self.log.emit(line)


class MainWindow(QMainWindow, Ui_MainWindow,QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setup UI
        self.setupUi(self)
        self.btn_run.pressed.connect(self.execute_program)
        self.btn_stop.pressed.connect(self.terminate_program)
    
    def start(self):
        if not self._worker.isRunning():
            self.process()

    def closeEvent(self, event):
        try:
            self.terminate_program()
        except:
            pass

    def toLog(self, txt):
        self.list_view.addItem(txt)

    def execute_program(self):
    
        self.user_input = self.line_edit_link.text()

        self.alert_message("Process Started!", "The process has started and the output will be generated in an excel file.")

        self.btn_stop.show()
        self.list_view.show()
        self.text_label.show()
        self.text_label.setText("Process Status:")
        self.proc = Process(target=main_caller, args=(self.user_input,))
        self.proc.start()
        self._worker = Thread(self)
        self._worker.log.connect(self.toLog)
        self._worker.start()

    def terminate_program(self):
        self.proc.terminate()
        self._worker.terminate()
        self.alert_message("Process Stopped!", "The Process has been stopped.")

    def alert_message(self, title, message):	
        if title == "Alert":	
            pass
        QMessageBox.information(self, title, message)