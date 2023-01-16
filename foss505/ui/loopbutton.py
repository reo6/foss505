from PySide6.QtWidgets import QLabel
from foss505.loop import Loop, LoopMode
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from typing import Any
from enum import Enum
from foss505.ui.get_asset import asset


DEFAULT_IMG_SIZE = (150, 150)

LoopPixmapTypes = Enum("LoopPixmapTypes", ["INACTIVE", "PLAY", "OVERDUB", "RECORD"])

def get_pixmap(type: LoopPixmapTypes): # FIXME: Recreate this structure.
    mapping = {
        LoopPixmapTypes.PLAY: QPixmap(asset("images/play.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopPixmapTypes.RECORD: QPixmap(asset("images/recording.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopPixmapTypes.OVERDUB: QPixmap(asset("images/overdub.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopPixmapTypes.INACTIVE: QPixmap(asset("images/inactive.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopPixmapTypes.MUTED: QPixmap(asset("images/muted.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
    }

    return mapping[type]

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

    def update_pixmap(self):
        if self.loop.take == [] and self.loop.mode != LoopMode.RECORD:
            self.setPixmap(get_pixmap(LoopPixmapTypes.INACTIVE))
        else:
            self.setPixmap(get_pixmap_from_loopmode(self.loop.mode))

    def on_hit(self, event: Any): # FIXME
        self.loop.toggle()
        self.update_pixmap()
