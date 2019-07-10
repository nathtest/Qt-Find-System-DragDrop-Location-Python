# Import the core and GUI elements of Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import fileWatcher


class MyTable(QTableWidget):
    # signal
    dropedFilesToUpload = pyqtSignal(list)

    def __init__(self, parent):
        super(MyTable, self).__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # disable cells
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # disable edits
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # only one cell select
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # right click context menu
        self.verticalHeader().setVisible(False)  # remove column row count
        self.setColumnCount(4)
        self.setRowCount(0)
        self.setHorizontalHeaderLabels(['Icon', 'Nom', 'Modifié le', 'Taille'])
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)

        self.file = None

        self.temp_path_outside_drag = os.path.normpath(r"C:\Windows\Temp")
        self.file_watcher_outside_drag = None

    def mimeData(self, items):
        data = QMimeData()

        urls = []
        i = 0
        for item in items:
            if i == 1:
                print("yo:" + item.text())
                path = os.path.join(self.temp_path_outside_drag, item.text())
                print(path)
                self.file = open(path, 'wb')  # create empty temp file
                self.file.close()
                self.file_watcher_outside_drag = fileWatcher.FileWatcher(path)  # watch temp file to find drop path
                self.file_watcher_outside_drag.start()
                self.file_watcher_outside_drag.newPathFounded.connect(self.dragOutsideConfirmed)  # signal

                urls.append(QUrl.fromLocalFile(path))
            i += 1

        data.setUrls(urls)
        return data

    @pyqtSlot(str)
    def dragOutsideConfirmed(self, outside_drop_path):
        print("Outside Drop path: " + outside_drop_path)
        self.file_watcher_outside_drag.stop()  # stop file watch

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print("drag enter")
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        print("drag move")
        event.accept()

    def dragLeaveEvent(self, event):
        print("drag leave")
        event.accept()

    def dropEvent(self, event):
        if event.source() != self:
            print("drop from outside")
            files = [(u.toLocalFile()) for u in event.mimeData().urls()]
            self.dropedFilesToUpload.emit(list(files))
            event.accept()
        print("inside")
        event.ignore()
