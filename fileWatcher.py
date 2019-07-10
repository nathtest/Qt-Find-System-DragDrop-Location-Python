#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32api
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class FileWatcher(FileSystemEventHandler, QObject):
    # signal
    newPathFounded = pyqtSignal(str)

    def __init__(self, filename):
        super(FileSystemEventHandler, self).__init__()
        QObject.__init__(self)

        # path = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        # for i in path:
        #     i = os.path.normpath(i)
        # print(path)
        self.fileToWatch_old_path = os.path.normpath(filename)
        self.fileToWatch_new_path = ""
        _, self.fileToWatch_filenane = os.path.split(self.fileToWatch_old_path)
        self.fileToWatch_deleted = False
        self.fileToWatch_created = False
        self.fileToWatch_moved = False
        self.observer = Observer()
        self.observer.schedule(self, path='C:/', recursive=True)
        print("File to watch: " + self.fileToWatch_old_path)
        print("Filename: " + self.fileToWatch_filenane)

    def start(self):
        self.observer.start()

    def stop(self):
        self.observer.stop()

    def join(self):
        self.observer.join()

    def on_created(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if os.path.normpath(event.src_path).find(self.fileToWatch_filenane) != -1 and self.fileToWatch_deleted is True:
            self.fileToWatch_created = True
            self.fileToWatch_moved = True
            self.fileToWatch_new_path = os.path.normpath(event.src_path)
            self.newPathFounded.emit(self.fileToWatch_new_path)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! file moved !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def on_deleted(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        if os.path.normpath(event.src_path).find(self.fileToWatch_old_path) != -1:
            self.fileToWatch_deleted = True


if __name__ == "__main__":
    filewatch = FileWatcher(r"C:\Users\Elfes\Desktop\ElfesFTPShare\upload_test_nath.txt")
    filewatch.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        filewatch.stop()
    filewatch.join()
