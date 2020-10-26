import os

from PySide2.QtCore import Property, Signal, Slot, QObject


class PerformanceService(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def setPerformance(self, percent):
        os.system("sudo sh -c 'echo %s > /sys/devices/system/cpu/intel_pstate/max_perf_pct'" % percent)

