from PySide6.QtWidgets import QSlider, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton
from foss505.loop import Loop, LoopMode
from PySide6.QtCore import Qt
import numpy as np
from typing import Callable
from foss505.exceptions import MuteError

def coef(gain):
    return 10**(gain/20)

def gain(coef):
    return 20 * np.log10(coef)

DB_LIMITS = (-30, 5)


class ToggleButton(QPushButton):
    """
    Toggle button base class.
    """
    def __init__(self):
        super().__init__()

        self.setCheckable(True)
        self.setStyleSheet("""
        QPushButton {
            background-color: #2A2550;
            color: #E04D01;
            font-weight: bold;
        }

        QPushButton:checked {
            background-color: #E04D01;
            color: #251D3A;
        }
        """)


class MuteButton(ToggleButton):
    def __init__(self, toggle_mute: Callable):
        super().__init__()

        self.toogle_mute = toggle_mute
        self.clicked.connect(toggle_mute)
        self.setText("M")


class ResetButton(QPushButton):
     def __init__(self, reset_take: Callable):
        super().__init__()

        self.clicked.connect(reset_take)
        self.setText("D")
        self.setStyleSheet("""
        QPushButton {
            background-color: #2A2550;
            color: #E04D01;
            font-weight: bold;
        }
        """)


class LoopVolumeBar(QWidget):
    def __init__(self, loop: Loop, slider_limits: tuple[int, int]= DB_LIMITS): # TODO: Revise this limit
        super().__init__()

        self.loop = loop
        self.slider_limits = slider_limits

        self.build_widgets()

    def build_widgets(self):
        """
        Build widgets of the LoopVolumeBar
        """
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

        buttons_layout = QHBoxLayout()
        self.mute_button = MuteButton(self.toggleMute)
        self.loop.mode.observe(self.updateMutedState)
        self.reset_button = ResetButton(self.resetTake)
        buttons_layout.addWidget(self.mute_button)
        buttons_layout.addWidget(self.reset_button)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def toggleMute(self):
        try:
            self.loop.toggle_mute()
        except MuteError:
            # This means that the loop is empty or in record/overdub mode.
            # clicked signal is emmited and checked, so make uncheck it:
            self.mute_button.setChecked(False)

    def resetTake(self):
        self.loop.reset_loop()

    def updateMutedState(self):
        """
        Observer for the loop mode, updates the mute button
        whenever the loop mode changes.
        """
        is_muted = self.loop.mode.value == LoopMode.MUTED
        self.mute_button.setChecked(is_muted)

    def sliderChanged(self, value):
        self.loop.gain = coef(value)
        self.updateLabel()

    def updateLabel(self):
        self.volume_label.setText(str(self.slider.value()) + " dB")
