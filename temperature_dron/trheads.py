# This Python file uses the following encoding: utf-8
from TransformFotos import TemperaturaMax
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool
import traceback


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        bool data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)

class threadMaxTemperatura(QRunnable, TemperaturaMax):

    def __init__(self, foto_temperatura, max_expected_temp):
        QRunnable.__init__(self)
        TemperaturaMax.__init__(self, max_expected_temp)
        self.signals = WorkerSignals()
        self.foto_temperatura = foto_temperatura

    @Slot()    
    def run(self):
        try:
           triger = self.is_max_trigger_foto(self.foto_temperatura)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(triger)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

