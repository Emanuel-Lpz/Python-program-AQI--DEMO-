import sys

from PySide6.QtWidgets import *

from aqi_data import AQI
from widgets import DropdownWidget, ChecklistWidget
from scoring import get_section_score


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("KB AQI Evaluator")

        self.resize(1600, 900)

        self.section_widgets = {}

        self.build_ui()

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        self.tabs = QTabWidget()

        layout.addWidget(self.tabs, 3)

        self.report = QTextEdit()
        self.report.setReadOnly(True)

        layout.addWidget(self.report, 1)

        for section_name, section_data in AQI.items():

            page = QWidget()

            page_layout = QVBoxLayout(page)

            self.section_widgets[section_name] = {}

            for criterion, data in section_data.items():

                if data["type"] == "dropdown":
                    widget = DropdownWidget(
                        criterion,
                        data
                    )
                else:
                    widget = ChecklistWidget(
                        criterion,
                        data
                    )

                page_layout.addWidget(widget)

                self.section_widgets[section_name][criterion] = widget

                self.connect_widget(widget)

            page_layout.addStretch()

            self.tabs.addTab(page, section_name)

        copy_btn = QPushButton(
            "Copy Report"
        )

        copy_btn.clicked.connect(
            self.copy_report
        )

        layout.addWidget(copy_btn)

        self.refresh()

    def connect_widget(self, widget):

        if hasattr(widget, "combo"):
            widget.combo.currentIndexChanged.connect(
                self.refresh
            )

        if hasattr(widget, "checks"):
            for cb, _ in widget.checks:
                cb.stateChanged.connect(
                    self.refresh
                )

    def refresh(self):

        total = 0

        lines = []

        for section, widgets in self.section_widgets.items():

            score = get_section_score(widgets)

            total += score

            lines.append(
                f"{section}: {score}"
            )

        lines.insert(
            0,
            f"TOTAL SCORE: {total}/100\n"
        )

        self.report.setText(
            "\n".join(lines)
        )

    def copy_report(self):

        QApplication.clipboard().setText(
            self.report.toPlainText()
        )


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()