from typing import Any

from PySide2.QtCore import QObject


class ListModelItem(QObject):
    roles = {
    }

    def __init__(self, parent=None, **kwargs):
        QObject.__init__(self, parent=parent)
        self._data = {key.encode(): value for key, value in kwargs.items()}

    def data(self, key: int) -> Any:
        return self._data[self.roles[key]]

    def roleData(self, key: bytes) -> Any:
        return self._data[key]
