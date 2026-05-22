import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import QColor

from aqi_data import AQI
from widgets import (
    DropdownWidget,
    ChecklistWidget
)

from scoring import (
    generate_report,
    check_auto_rejects
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "KB AQI Evaluator"
        )

        self.resize(1700, 950)

        self.section_widgets = {}

        self.build_ui()

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        self.tabs = QTabWidget()

        main_layout.addWidget(
            self.tabs,
            3
        )

        right_panel = QVBoxLayout()

        main_layout.addLayout(
            right_panel,
            1
        )

        self.report_box = QTextEdit()

        self.report_box.setReadOnly(True)

        right_panel.addWidget(
            self.report_box
        )

        self.warning_label = QLabel()

        self.warning_label.setStyleSheet(
            "color: red; font-weight: bold;"
        )

        right_panel.addWidget(
            self.warning_label
        )

        self.missing_label = QLabel()

        self.missing_label.setStyleSheet(
            "color: orange;"
        )

        right_panel.addWidget(
            self.missing_label
        )

        generate_btn = QPushButton(
            "Generate Report"
        )

        generate_btn.clicked.connect(
            self.refresh_report
        )

        right_panel.addWidget(
            generate_btn
        )

        copy_btn = QPushButton(
            "Copy Report"
        )

        copy_btn.clicked.connect(
            self.copy_report
        )

        right_panel.addWidget(
            copy_btn
        )

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

                page_layout.addWidget(
                    widget
                )

                self.section_widgets[
                    section_name
                ][criterion] = widget

                self.connect_widget(widget)

            page_layout.addStretch()

            scroll = QScrollArea()

            scroll.setWidgetResizable(True)

            scroll.setWidget(page)

            self.tabs.addTab(
                scroll,
                section_name
            )

        self.refresh_report()

    def connect_widget(self, widget):

        if hasattr(widget, "combo"):

            widget.combo.currentIndexChanged.connect(
                self.refresh_report
            )

        if hasattr(widget, "checks"):

            for cb, _, _ in widget.checks:

                cb.stateChanged.connect(
                    self.refresh_report
                )

    def count_missing_fields(self):

        missing = 0

        for _, widgets in self.section_widgets.items():

            for _, widget in widgets.items():

                if not widget.is_complete():

                    missing += 1

        return missing

    def refresh_report(self):

        report = generate_report(
            self.section_widgets,
            AQI
        )

        self.report_box.setText(
            report
        )

        errors = check_auto_rejects(
            self.section_widgets,
            AQI
        )

        if errors:

            text = (
                "🚨 AUTO-REJECT WARNING\n\n"
                "KB does not comply "
                "with KCS requirements.\n\n"
                "Issues:\n"
            )

            for err in errors:

                text += f"• {err}\n"

            self.warning_label.setText(
                text
            )

        else:

            self.warning_label.setText("")

        missing = self.count_missing_fields()

        if missing > 0:

            self.missing_label.setText(
                f"⚠ {missing} field(s) "
                f"have not been evaluated."
            )

        else:

            self.missing_label.setText(
                ""
            )

    def copy_report(self):

        QApplication.clipboard().setText(
            self.report_box.toPlainText()
        )


app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()