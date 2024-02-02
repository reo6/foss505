"""
Represents loop channels on the UI.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from foss505.loop import Loop
from PySide6.QtCore import Qt
from foss505.ui.loopbutton import LoopButton
from foss505.ui.volumebar import LoopVolumeBar


class LoopChannel(QWidget):
    def __init__(self, loop: Loop):
        super().__init__()

        self.loop = loop
        self.build_widgets()

    def build_widgets(self):
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        self.volumebar = LoopVolumeBar(self.loop)
        main_layout.addWidget(self.volumebar)

        self.loopbutton = LoopButton(self.loop)
        main_layout.addWidget(self.loopbutton)



        self.setLayout(main_layout)
