from PySide6.QtWidgets import QSlider, QVBoxLayout, QWidget, QLabel
from foss505.loop import Loop
from PySide6.QtCore import Qt
import numpy as np

def coef(gain):
    return 10**(gain/20)

def gain(coef):
    return 20 * np.log10(coef)

DB_LIMITS = (-30, 5)

class LoopVolumeBar(QWidget):
    def __init__(self, loop: Loop, slider_limits: tuple[int, int]= DB_LIMITS): # TODO: Revise this limit
        super().__init__()

        self.loop = loop
        self.muted = False
        self.slider_limits = slider_limits

        self.build_widgets()

    def build_widgets(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        self.slider = QSlider()
        self.slider.setRange(*self.slider_limits)
        self.slider.setSingleStep(1)
        self.slider.setValue(gain(self.loop.gain))
        self.slider.valueChanged.connect(self.sliderChanged)
        self.slider.setStyleSheet("""
        QSlider::handle:vertical {
            background-color: #E04D01;
            border-radius: 3px;
        }
        QSlider::groove:vertical {
            height: 16px;
        }

        QSlider::add-page:vertical {
            background-color: #E04D01;
        }

        QSlider::sub-page:vertical {
            background-color: #2A2550;
        }
        """)
        main_layout.addWidget(self.slider, alignment=Qt.AlignCenter)

        self.volume_label = QLabel()
        self.updateLabel()
        main_layout.addWidget(self.volume_label)

        self.setLayout(main_layout)

    def sliderChanged(self, value):
        if self.muted:
            self.loop.gain = 0
        else:
            self.loop.gain = coef(value)

        self.updateLabel()

    def updateLabel(self):
        self.volume_label.setText(str(self.slider.value()) + " dB")
