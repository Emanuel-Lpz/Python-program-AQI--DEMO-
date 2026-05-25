import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
    QTextEdit,
    QLabel,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QFrame
)

from aqi_data import AQI

from widgets import (
    DropdownWidget,
    ChecklistWidget
)

from scoring import (
    generate_report,
    generate_dashboard,
    check_auto_rejects,
    get_total_score
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "KB AQI Evaluator"
        )

        self.resize(
            1800,
            1000
        )

        self.section_widgets = {}

        self.build_ui()

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QHBoxLayout(
            central
        )

        # ------------------------------------------
        # LEFT SIDE (AQI TABS)
        # ------------------------------------------

        left_panel = QVBoxLayout()

        self.tabs = QTabWidget()

        left_panel.addWidget(
            self.tabs,
            1
        )

        left_panel.addStretch()

        self.help_label = QLabel(
            "Green text highlights mandatory criteria that may generate an Auto-reject"
        )

        self.help_label.setWordWrap(True)

        self.help_label.setStyleSheet(
            "color: gray; font-size:11px; padding:2px 4px 2px 4px; margin:0;"
        )

        self.help_label.setMaximumHeight(24)

        left_panel.addWidget(
            self.help_label
        )

        main_layout.addLayout(
            left_panel,
            3
        )

        # ------------------------------------------
        # RIGHT SIDE
        # ------------------------------------------

        right_panel = QVBoxLayout()

        main_layout.addLayout(
            right_panel,
            1
        )

        # ------------------------------------------
        # SCORE HEADER
        # ------------------------------------------

        self.score_label = QLabel(
            "AQI SCORE: 0/100"
        )

        self.score_label.setStyleSheet(
            """
            font-size:18px;
            font-weight:bold;
            padding:6px;
            """
        )

        right_panel.addWidget(
            self.score_label
        )

        # ------------------------------------------
        # DASHBOARD
        # ------------------------------------------

        dashboard_title = QLabel(
            "<b>Dashboard</b>"
        )

        right_panel.addWidget(
            dashboard_title
        )

        self.dashboard_box = QTextEdit()

        self.dashboard_box.setReadOnly(
            True
        )

        self.dashboard_box.setMaximumHeight(
            220
        )

        right_panel.addWidget(
            self.dashboard_box
        )

        # ------------------------------------------
        # AUTO REJECT
        # ------------------------------------------

        self.warning_label = QLabel()

        self.warning_label.setWordWrap(
            True
        )

        self.warning_label.setStyleSheet(
            """
            color:#B22222;
            font-weight:bold;
            """
        )

        right_panel.addWidget(
            self.warning_label
        )

        # ------------------------------------------
        # MISSING FIELDS
        # ------------------------------------------

        self.missing_label = QLabel()

        self.missing_label.setWordWrap(
            True
        )

        self.missing_label.setStyleSheet(
            """
            color:orange;
            font-weight:bold;
            """
        )

        right_panel.addWidget(
            self.missing_label
        )

        line = QFrame()

        line.setFrameShape(
            QFrame.Shape.HLine
        )

        right_panel.addWidget(
            line
        )

        # ------------------------------------------
        # REPORT
        # ------------------------------------------

        report_title = QLabel(
            "<b>Detailed Report</b>"
        )

        right_panel.addWidget(
            report_title
        )

        self.report_box = QTextEdit()

        self.report_box.setReadOnly(
            True
        )

        right_panel.addWidget(
            self.report_box
        )

        # ------------------------------------------
        # BUTTONS
        # ------------------------------------------

        copy_btn = QPushButton(
            "Copy Report"
        )

        copy_btn.clicked.connect(
            self.copy_report
        )

        right_panel.addWidget(
            copy_btn
        )

        reset_btn = QPushButton(
            "Reset AQI"
        )

        reset_btn.clicked.connect(
            self.reset_aqi
        )

        right_panel.addWidget(
            reset_btn
        )

        # ==================================================
        # BUILD TABS
        # ==================================================

        for (
            section_name,
            section_data
        ) in AQI.items():

            page = QWidget()

            page_layout = QVBoxLayout(
                page
            )

            self.section_widgets[
                section_name
            ] = {}

            for (
                criterion,
                data
            ) in section_data.items():

                if (
                    data["type"]
                    == "dropdown"
                ):

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

                self.connect_widget(
                    widget
                )

            page_layout.addStretch()

            scroll = QScrollArea()

            scroll.setWidgetResizable(
                True
            )

            scroll.setWidget(
                page
            )

            self.tabs.addTab(
                scroll,
                section_name
            )

        self.refresh_report()

    # ==================================================
    # SIGNALS
    # ==================================================

    def connect_widget(
        self,
        widget
    ):

        if hasattr(
            widget,
            "combo"
        ):

            widget.combo.currentIndexChanged.connect(
                self.refresh_report
            )

        if hasattr(
            widget,
            "checks"
        ):

            for (
                cb,
                _,
                _
            ) in widget.checks:

                cb.stateChanged.connect(
                    self.refresh_report
                )

    # ==================================================
    # MISSING FIELDS
    # ==================================================

    def count_missing_fields(
        self
    ):

        missing = 0

        for widgets in (
            self.section_widgets.values()
        ):

            for widget in (
                widgets.values()
            ):

                if (
                    not widget.is_complete()
                ):

                    missing += 1

        return missing

    # ==================================================
    # SCORE COLOR
    # ==================================================

    def update_score_color(
        self,
        score
    ):

        if score >= 95:

            color = "#228B22"

        elif score >= 85:

            color = "#DAA520"

        else:

            color = "#B22222"

        self.score_label.setStyleSheet(
            f"""
            color:{color};
            font-size:18px;
            font-weight:bold;
            padding:6px;
            """
        )

    # ==================================================
    # REFRESH
    # ==================================================

    def refresh_report(
        self
    ):

        report = generate_report(
            self.section_widgets,
            AQI
        )

        dashboard = generate_dashboard(
            self.section_widgets,
            AQI
        )

        total_score = get_total_score(
            self.section_widgets
        )

        self.score_label.setText(
            f"AQI SCORE: "
            f"{total_score}/100"
        )

        self.update_score_color(
            total_score
        )

        self.report_box.setText(
            report
        )

        self.dashboard_box.setText(
            dashboard
        )

        # ----------------------------------
        # Auto Reject
        # ----------------------------------

        errors = check_auto_rejects(
            self.section_widgets,
            AQI
        )

        if errors:

            text = (
                "🚨 AUTO-REJECT WARNING\n\n"
                "This KB does not currently "
                "comply with mandatory AQI/KCS "
                "requirements.\n\n"
                "Issues:\n"
            )

            for err in errors:

                text += (
                    f"• {err}\n"
                )

            self.warning_label.setText(
                text
            )

        else:

            self.warning_label.setText(
                ""
            )

        # ----------------------------------
        # Missing Fields
        # ----------------------------------

        missing = (
            self.count_missing_fields()
        )

        if missing:

            self.missing_label.setText(
                f"⚠ {missing} field(s) "
                f"have not been evaluated."
            )

        else:

            self.missing_label.setText(
                "✓ All fields evaluated."
            )

    # ==================================================
    # COPY REPORT
    # ==================================================

    def copy_report(
        self
    ):

        QApplication.clipboard().setText(
            self.report_box.toPlainText()
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset_aqi(
        self
    ):

        answer = QMessageBox.question(
            self,
            "Confirm Reset",
            "Are you sure you want to reset the AQI evaluation?\nAll selections will be cleared.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        for widgets in self.section_widgets.values():

            for widget in widgets.values():

                if hasattr(widget, "combo"):

                    widget.combo.setCurrentIndex(0)

                if hasattr(widget, "checks"):

                    for cb, _, _ in widget.checks:

                        cb.setChecked(False)

        self.tabs.setCurrentIndex(0)
        self.refresh_report()


# ======================================================
# MAIN
# ======================================================

app = QApplication(
    sys.argv
)

window = MainWindow()

window.show()

app.exec()