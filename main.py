import sys

from PySide6.QtCore import Qt
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
    QCheckBox,
    QMessageBox,
    QScrollArea,
    QFrame,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QLineEdit
)

from aqi_data import AQI

from widgets import (
    DropdownWidget,
    ChecklistWidget,
    CheckboxWidget
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
            900,
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
            "color: white; font-size:11px; padding:2px 4px 2px 4px; margin:0;"
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

        self.score_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.score_label.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            padding:12px;
            border:2px solid #444;
            border-radius:12px;
            background-color:#161616;
            """
        )

        right_panel.addWidget(
            self.score_label
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

        # ------------------------------------------
        # REPORT
        # ------------------------------------------

        report_header = QHBoxLayout()

        self.report_title = QLabel(
            "<b>Generated Report</b>"
        )

        self.summary_checkbox = QCheckBox(
            "Summarized"
        )

        self.summary_checkbox.setChecked(False)

        self.summary_checkbox.toggled.connect(
            self.update_report_view
        )

        report_header.addWidget(
            self.report_title
        )

        report_header.addStretch()

        report_header.addWidget(
            self.summary_checkbox
        )

        right_panel.addLayout(
            report_header
        )

        line = QFrame()

        line.setFrameShape(
            QFrame.Shape.HLine
        )

        right_panel.addWidget(
            line
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

        manage_notes_btn = QPushButton(
            "Manage Notes"
        )

        manage_notes_btn.clicked.connect(
            self.open_notes_manager
        )

        right_panel.addWidget(
            manage_notes_btn
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
            color:orange;
            font-weight:bold;
            """
        )

        right_panel.addWidget(
            self.warning_label
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

                elif (
                    data["type"]
                    == "checkbox"
                ):

                    widget = CheckboxWidget(
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
            "noteChanged"
        ):
            widget.noteChanged.connect(
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

                if hasattr(
                    cb,
                    "noteChanged"
                ):
                    cb.noteChanged.connect(
                        self.refresh_report
                    )

                if hasattr(
                    cb,
                    "noteChanged"
                ):
                    cb.noteChanged.connect(
                        self.refresh_report
                    )

        if hasattr(
            widget,
            "checkbox"
        ):

            widget.checkbox.stateChanged.connect(
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
            font-size:28px;
            font-weight:bold;
            padding:12px;
            border:2px solid #444;
            border-radius:12px;
            background-color:#161616;
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

        self.detailed_text = report
        self.summary_text = dashboard

        self.update_report_view()

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

            self.missing_label.setStyleSheet(
                """
                color:orange;
                font-weight:bold;
                """
            )

            self.missing_label.setText(
                f"⚠ {missing} field(s) "
                f"have not been evaluated."
            )

        else:

            self.missing_label.setStyleSheet(
                """
                color:#00AD7C;
                font-weight:bold;
                """
            )

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
    # NOTE MANAGER
    # ==================================================

    def open_notes_manager(
        self
    ):

        dialog = NotesManagerDialog(
            self,
            self.section_widgets
        )

        dialog.exec()
        self.refresh_report()

    # ==================================================
    # VIEW TOGGLE
    # ==================================================

    def update_report_view(
        self
    ):

        show_summary = self.summary_checkbox.isChecked()

        self.report_box.setText(
            self.summary_text
            if show_summary
            else self.detailed_text
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

                if hasattr(widget, "note"):

                    widget.note = None

        self.tabs.setCurrentIndex(0)
        self.refresh_report()


class NoteEditorDialog(QDialog):

    MAX_LENGTH = 200

    def __init__(self, parent, title, note=""):

        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)

        instructions = QLabel(
            "Enter up to 200 characters for this note."
        )

        layout.addWidget(instructions)

        self.text_edit = QLineEdit()
        self.text_edit.setText(note)
        self.text_edit.setMaxLength(self.MAX_LENGTH)
        self.text_edit.textChanged.connect(self.update_count)
        self.text_edit.returnPressed.connect(self.accept)

        layout.addWidget(self.text_edit)

        self.count_label = QLabel()
        layout.addWidget(self.count_label)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        save_btn.setDefault(True)
        save_btn.setAutoDefault(True)
        cancel_btn.setAutoDefault(False)

        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self.accept)

        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

        self.update_count()

    def update_count(self):

        text = self.text_edit.text()

        if len(text) > self.MAX_LENGTH:
            text = text[: self.MAX_LENGTH]
            self.text_edit.blockSignals(True)
            self.text_edit.setText(text)
            self.text_edit.blockSignals(False)

        self.count_label.setText(
            f"{len(text)}/{self.MAX_LENGTH} characters"
        )

    def get_text(self):

        return self.text_edit.text().strip()


class NotesManagerDialog(QDialog):

    def __init__(self, parent, section_widgets):

        super().__init__(parent)

        self.section_widgets = section_widgets

        self.setWindowTitle("Manage Notes")
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        self.list_widget.currentItemChanged.connect(
            self.update_preview
        )

        layout.addWidget(self.list_widget)

        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setFixedHeight(120)

        layout.addWidget(QLabel("Selected note content:"))
        layout.addWidget(self.preview)

        button_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        delete_all_btn = QPushButton("Delete All")
        close_btn = QPushButton("Close")

        self.edit_btn.clicked.connect(
            self.edit_selected_note
        )
        self.delete_btn.clicked.connect(
            self.delete_selected_note
        )
        delete_all_btn.clicked.connect(
            self.delete_all_notes
        )
        close_btn.clicked.connect(self.accept)

        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(delete_all_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        self.refresh_list()

    def refresh_list(self):

        self.list_widget.clear()

        for section_name, widgets in self.section_widgets.items():
            for criterion, widget in widgets.items():
                note = getattr(widget, "note", None)
                if note:
                    item = QListWidgetItem(
                        f"{section_name} > {criterion}"
                    )
                    item.setData(
                        Qt.UserRole,
                        (section_name, criterion, widget)
                    )
                    self.list_widget.addItem(item)

        self.update_preview()
        self.update_buttons()

    def update_buttons(self):

        has_selection = (
            self.list_widget.currentItem() is not None
        )

        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def update_preview(self):

        item = self.list_widget.currentItem()

        if not item:
            self.preview.setPlainText(
                "No note selected."
            )
            self.update_buttons()
            return

        _, _, widget = item.data(Qt.UserRole)
        self.preview.setPlainText(
            getattr(widget, "note", "")
        )
        self.update_buttons()

    def get_selected_widget(self):

        item = self.list_widget.currentItem()

        if not item:
            return None

        return item.data(Qt.UserRole)[2]

    def edit_selected_note(self):

        widget = self.get_selected_widget()
        if widget is None:
            return

        dialog = NoteEditorDialog(
            self,
            f"Edit note for {widget.title}",
            getattr(widget, "note", "")
        )

        if dialog.exec() == QDialog.Accepted:
            widget.note = dialog.get_text() or None
            self.refresh_list()

    def delete_selected_note(self):

        widget = self.get_selected_widget()
        if widget is None:
            return

        widget.note = None
        self.refresh_list()

    def delete_all_notes(self):

        for widgets in self.section_widgets.values():
            for widget in widgets.values():
                widget.note = None

        self.refresh_list()


# ======================================================
# MAIN
# ======================================================

app = QApplication(
    sys.argv
)

window = MainWindow()

window.show()

app.exec()