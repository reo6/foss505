from PySide6.QtWidgets import QLabel
from foss505.loop import Loop, LoopMode
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from typing import Any
from enum import Enum
from foss505.ui.get_asset import asset


DEFAULT_IMG_SIZE = (150, 150)

def get_pixmap(type_: LoopMode):
    mapping = {
        LoopMode.PLAY: QPixmap(asset("images/play.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopMode.RECORD: QPixmap(asset("images/recording.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopMode.OVERDUB: QPixmap(asset("images/overdub.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopMode.MUTED: QPixmap(asset("images/muted.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
        LoopMode.EMPTY: QPixmap(asset("images/inactive.png")).scaled(*DEFAULT_IMG_SIZE, Qt.KeepAspectRatio),
    }

    return mapping[type_]


class LoopButton(QLabel):
    def __init__(self, loop: Loop):
        super().__init__()

        self.loop = loop
        self.update_pixmap()
        self.setAlignment(Qt.AlignCenter)
        self.mousePressEvent = self.on_hit
        self.loop.mode.observe(self.update_pixmap)

    def update_pixmap(self):
        self.setPixmap(get_pixmap(self.loop.mode.value))

    def on_hit(self, event: Any): # FIXME
        self.loop.toggle()
