from functools import singledispatch
from typing import Any, List, Union, Type, Iterable, Sequence

from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import QModelIndex

from libs.ListModelItem import ListModelItem


class ListModel(QAbstractListModel):
    def __init__(self, prototype: ListModelItem, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.parent = parent
        self._prototype = prototype
        self._items: List[ListModelItem] = []

    def roleNames(self):
        return self._prototype.roles

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index: QModelIndex, role: int) -> Any:
        return self._items[index.row()].data(role)

    def clear(self):
        #self.beginResetModel()
        del self._items[:]
        #self.endResetModel()
        #self._items = []

    def indexOf(self, role: bytes, value: Any):
        return next((idx for idx, item in enumerate(self._items) if item.roleData(role) == value))

    def addItem(self, item: ListModelItem):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append(item)
        self.endInsertRows()

    def addItems(self, items: List[ListModelItem]):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + len(items) - 1)
        self._items.extend(items)
        self.endInsertRows()

    def removeIndex(self, idx: int):
        self.beginRemoveRows(QModelIndex(), idx, idx)
        del self._items[idx]
        self.endRemoveRows()
