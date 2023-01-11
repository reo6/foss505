from PySide6.QtWidgets import QLabel
from foss505.loop import Loop, LoopMode
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from typing import Any
from enum import Enum


DEFAULT_IMG_SIZE = (150, 150)

LoopPixmapTypes = Enum("LoopPixmapTypes", ["INACTIVE", "PLAY", "OVERDUB", "RECORD"])

def get_pixmap(type: LoopPixmapTypes): # FIXME: Recreate this structure.
    if type == LoopPixmapTypes.INACTIVE:
        return QPixmap("foss505/ui/assets/images/inactive.png").scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio)
    if type == LoopPixmapTypes.PLAY:
        return QPixmap("foss505/ui/assets/images/play.png").scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio)
    if type == LoopPixmapTypes.OVERDUB:
        return QPixmap("foss505/ui/assets/images/overdub.png").scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio)
    if type == LoopPixmapTypes.RECORD:
        return QPixmap("foss505/ui/assets/images/record.png").scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio)

def get_pixmap_from_loopmode(mode: LoopMode):
    mapping = {
        LoopMode.PLAY: LoopPixmapTypes.PLAY,
        LoopMode.RECORD: LoopPixmapTypes.RECORD,
        LoopMode.OVERDUB: LoopPixmapTypes.OVERDUB,
    } # FIXME

    return get_pixmap(mapping[mode])

class LoopButton(QLabel):
    def __init__(self, loop: Loop):
        super().__init__()

        self.loop = loop
        self.setPixmap(get_pixmap(LoopPixmapTypes.INACTIVE))
        self.setAlignment(Qt.AlignCenter)
        self.mousePressEvent = self.on_hit

    def set_mode(self, mode: LoopMode):
        self.loop.mode = mode
        self.update_pixmap()
        print(f"Log: Mode set to {mode}")

    def update_pixmap(self):
        if self.loop.take == []:
            self.setPixmap(get_pixmap(LoopPixmapTypes.INACTIVE))
            return

        self.setPixmap(get_pixmap_from_loopmode(self.loop.mode))

    def on_hit(self, event: Any): # FIXME
        if self.loop.take == [] and self.loop.mode == LoopMode.PLAY:
            self.set_mode(LoopMode.RECORD)
        elif self.loop.mode == LoopMode.PLAY:
            self.set_mode(LoopMode.OVERDUB)
        elif self.loop.mode == LoopMode.RECORD or self.loop.mode == LoopMode.OVERDUB:
            self.set_mode(LoopMode.PLAY)
