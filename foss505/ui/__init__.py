from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PySide6.QtCore import Qt
import sys
from foss505.station import Station, LOOP_CHANNEL_SIZE
from foss505.ui.loopchannel import LoopChannel
from foss505.ui.get_asset import asset


class LooperUI(QMainWindow):
    def __init__(self, station: Station):
        super().__init__()
        self.station = station

        self.setWindowTitle("Foss505")
        self.setWindowIcon(QIcon(asset("images/logo.png")))

        # Load the font.
        QFontDatabase.addApplicationFont(asset("fonts/KaushanScript-Regular.ttf"))

        # Build the widgets.
        self.build_widgets()

    def build_widgets(self):
        main_layout = QVBoxLayout()

        title = QLabel("foss505")
        title.setFont(QFont("KaushanScript", 40))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #E04D01;")
        main_layout.addWidget(title)

        ### Generate Loop channel areas.
        loop_channels = QHBoxLayout()
        main_layout.addLayout(loop_channels)
        loop_channels.setAlignment(Qt.AlignCenter)

        for loopch in self.station.loop_channels:
            loopch_widget = LoopChannel(loopch)
            loop_channels.addWidget(loopch_widget)

        #loopbtn = QLabel("")
        #loopbtn.setPixmap(QPixmap(LOOPBUTTON_IMAGE))
        #loopbtn.setAlignment(Qt.AlignCenter)
        #main_layout.addWidget(loopbtn)

        widget = QWidget()
        widget.setLayout(main_layout)
        widget.setStyleSheet("background-color: #251D3A;")
        self.setCentralWidget(widget)


def run_ui(station: Station):
    app = QApplication(sys.argv)

    window = LooperUI(station)
    window.show()

    app.exec_()
