from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox,
    QMenu,
    QDialog,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)

AUTO_REJECT_COLOR = "#00AD7C"


class HeaderLabel(QLabel):

    noteRequested = Signal()

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        add_note = menu.addAction(
            "Add note"
        )

        action = menu.exec(
            event.globalPos()
        )

        if action == add_note:
            self.noteRequested.emit()


class NoteDialog(QDialog):

    MAX_LENGTH = 200

    def __init__(self, title, note="", parent=None):

        super().__init__(parent)

        self.setWindowTitle(title)
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)

        label = QLabel(
            "Add or edit the note for this field."
        )

        layout.addWidget(label)

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


class DropdownWidget(QWidget):

    noteChanged = Signal()

    def __init__(self, title, data):

        super().__init__()

        self.title = title
        self.data = data
        self.note = None

        layout = QVBoxLayout(self)

        # ----------------------------
        # Title
        # ----------------------------

        title_text = title

        if data.get("auto_reject"):
            title_text = title

        title_label = HeaderLabel(
            f"<b>{title_text}</b>"
        )

        title_label.noteRequested.connect(
            self.prompt_note
        )

        if data.get("auto_reject"):

            title_label.setStyleSheet(
                f"color:{AUTO_REJECT_COLOR};"
            )

            title_label.setToolTip(
                "AUTO-REJECT CRITERION\n\n"
                "Failing this criterion causes "
                "automatic rejection of the KB."
            )

        layout.addWidget(title_label)

        # ----------------------------
        # Dropdown
        # ----------------------------

        self.combo = QComboBox()

        self.combo.addItem(
            "-- Select an option --",
            None
        )

        for text, score in data["options"]:

            display = (
                f"{text} ({score:+d})"
            )

            self.combo.addItem(
                display,
                score
            )

        self.combo.setCurrentIndex(0)

        layout.addWidget(self.combo)

        # ----------------------------
        # Description
        # ----------------------------

        desc = QLabel(
            data["description"]
        )

        desc.setWordWrap(True)

        desc.setStyleSheet(
            "color: gray;"
        )

        layout.addWidget(desc)

    # --------------------------------
    # Score
    # --------------------------------

    def get_score(self):

        value = self.combo.currentData()

        if value is None:
            return 0

        return value

    def get_max_score(self):

        return max(
            score
            for _, score
            in self.data["options"]
        )

    def prompt_note(self):

        dialog = NoteDialog(
            f"Add note for {self.title}",
            self.note,
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return

        note = dialog.get_text()

        self.note = note if note else None
        self.noteChanged.emit()

    def get_note_lines(self):

        if not self.note:
            return []

        lost = self.get_score() - self.get_max_score()

        return [
            f"{self.title} ({lost:+d}) - {self.note}"
        ]

    # --------------------------------
    # Missing field check
    # --------------------------------

    def is_complete(self):

        return (
            self.combo.currentData()
            is not None
        )

    # --------------------------------
    # Selected?
    # --------------------------------

    def is_selected(self):

        return self.combo.currentData() is not None


class CheckboxWidget(QWidget):

    noteChanged = Signal()

    def __init__(self, title, data):

        super().__init__()

        self.title = title
        self.data = data
        self.note = None

        layout = QVBoxLayout(self)

        title_label = HeaderLabel(
            f"<b>{title}</b>"
        )

        title_label.noteRequested.connect(
            self.prompt_note
        )

        layout.addWidget(title_label)

        label, score = self.data["options"][0]

        self.checkbox = QCheckBox(
            f"{label} ({score:+d})"
        )

        layout.addWidget(self.checkbox)

        desc = QLabel(
            self.data["description"]
        )

        desc.setWordWrap(True)
        desc.setStyleSheet("color: gray;")

        layout.addWidget(desc)

    def get_score(self):

        if self.checkbox.isChecked():
            return self.data["options"][0][1]

        return 0

    def get_max_score(self):

        return max(
            score
            for _, score
            in self.data["options"]
        )

    def prompt_note(self):

        dialog = NoteDialog(
            f"Add note for {self.title}",
            self.note,
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return

        note = dialog.get_text()

        self.note = note if note else None
        self.noteChanged.emit()

    def get_note_lines(self):

        if not self.note:
            return []

        lost = self.get_score() - self.get_max_score()

        return [
            f"{self.title} ({lost:+d}) - {self.note}"
        ]

    def is_complete(self):

        return True

    def is_selected(self):

        return True


class ChecklistWidget(QWidget):

    noteChanged = Signal()

    def __init__(self, title, data):

        super().__init__()

        self.title = title
        self.data = data
        self.note = None

        self.checks = []
        self.not_applicable_checkbox = None
        self.not_applicable_data = data.get("not_applicable")
        self.not_applicable_items = data.get(
            "not_applicable_items",
            []
        )

        layout = QVBoxLayout(self)

        # ----------------------------
        # Title
        # ----------------------------

        title_text = title

        if data.get(
            "auto_reject_items"
        ):
            title_text = title

        title_label = HeaderLabel(
            f"<b>{title_text}</b>"
        )

        title_label.noteRequested.connect(
            self.prompt_note
        )

        if data.get(
            "auto_reject_items"
        ):

            title_label.setStyleSheet(
                f"color:{AUTO_REJECT_COLOR};"
            )

            title_label.setToolTip(
                "Contains AUTO-REJECT checks."
            )

        layout.addWidget(
            title_label
        )

        # ----------------------------
        # Description
        # ----------------------------

        desc = QLabel(
            data["description"]
        )

        desc.setWordWrap(True)

        desc.setStyleSheet(
            "color: gray;"
        )

        layout.addWidget(desc)

        # ----------------------------
        # Checklist items
        # ----------------------------

        auto_items = data.get(
            "auto_reject_items",
            []
        )

        primary_items = []
        attachment_items = []

        for text, score in data["items"]:
            if text in self.not_applicable_items:
                attachment_items.append((text, score))
            else:
                primary_items.append((text, score))

        for text, score in primary_items:
            cb = QCheckBox(
                f"{text} ({score:+d})"
            )

            style = ""

            if self.not_applicable_data:
                style += "margin-left:18px;"

            if text in auto_items:
                style += f"color:{AUTO_REJECT_COLOR};"
                cb.setToolTip(
                    "AUTO-REJECT item.\n\n"
                    "If this checkbox is not satisfied "
                    "the KB must be rejected."
                )

            if style:
                cb.setStyleSheet(style)

            layout.addWidget(cb)

            self.checks.append(
                (
                    cb,
                    text,
                    score,
                    text in self.not_applicable_items
                )
            )

        if self.not_applicable_data and self.not_applicable_items:
            na_label, na_score = self.not_applicable_data
            self.not_applicable_checkbox = QCheckBox(
                f"{na_label} ({na_score:+d})"
            )
            self.not_applicable_checkbox.setStyleSheet(
                "font-weight:bold;"
            )
            self.not_applicable_checkbox.toggled.connect(
                self.on_not_applicable_toggled
            )
            layout.addWidget(self.not_applicable_checkbox)

        for text, score in attachment_items:
            cb = QCheckBox(
                f"{text} ({score:+d})"
            )

            style = ""

            if self.not_applicable_data:
                style += "margin-left:18px;"

            if text in auto_items:
                style += f"color:{AUTO_REJECT_COLOR};"
                cb.setToolTip(
                    "AUTO-REJECT item.\n\n"
                    "If this checkbox is not satisfied "
                    "the KB must be rejected."
                )

            if style:
                cb.setStyleSheet(style)

            layout.addWidget(cb)

            self.checks.append(
                (
                    cb,
                    text,
                    score,
                    text in self.not_applicable_items
                )
            )

    # --------------------------------
    # Score
    # --------------------------------

    def get_score(self):
        # If the parent "not applicable" box is checked, some checklists
        # should award the not_applicable score AND still include any
        # primary (non-attachment) checked items. If there are no
        # not_applicable_items configured, treat the parent as replacing
        # the whole checklist (legacy behaviour).

        if self.is_not_applicable():
            parent_score = self.not_applicable_data[1]

            # If there are specific items marked as 'not_applicable_items'
            # only include primary (non-attachment) checked items in
            # addition to the parent score.
            if self.not_applicable_items:
                extra = 0
                for cb, _, points, is_attachment in self.checks:
                    if not is_attachment and cb.isChecked():
                        extra += points

                return max(parent_score + extra, 0)

            # Fallback: parent replaces entire checklist
            return max(parent_score, 0)

        score = 0

        for cb, _, points, _ in self.checks:
            if cb.isChecked():
                score += points

        return max(score, 0)

    def get_max_score(self):
        # When there are not_applicable_items defined, the maximum should
        # reflect the parent not-applicable score plus the maximum of the
        # primary (non-attachment) items. Otherwise sum all positive items
        # (legacy behaviour).

        if self.not_applicable_items:
            parent = self.not_applicable_data[1] if self.not_applicable_data else 0
            primary_max = sum(
                score
                for text, score in self.data["items"]
                if score > 0 and text not in self.not_applicable_items
            )

            return parent + primary_max

        return sum(
            score
            for _, score in self.data["items"]
            if score > 0
        )

    def prompt_note(self):

        dialog = NoteDialog(
            f"Add note for {self.title}",
            self.note,
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return

        note = dialog.get_text()

        self.note = note if note else None
        self.noteChanged.emit()

    def get_note_lines(self):

        if not self.note:
            return []

        lost = self.get_score() - self.get_max_score()

        return [
            f"{self.title} ({lost:+d}) - {self.note}"
        ]

    # --------------------------------
    # Missing field check
    # --------------------------------

    def is_not_applicable(self):

        return (
            self.not_applicable_checkbox is not None
            and self.not_applicable_checkbox.isChecked()
        )

    def is_complete(self):

        if self.is_not_applicable():
            return True

        return any(
            cb.isChecked()
            for cb, _, _, _
            in self.checks
        )

    def on_not_applicable_toggled(self, checked):

        for cb, _, _, is_attachment in self.checks:
            if self.not_applicable_items:
                if is_attachment:
                    cb.setVisible(not checked)
                    if checked:
                        cb.setChecked(False)
            else:
                cb.setVisible(not checked)
                if checked:
                    cb.setChecked(False)

        self.noteChanged.emit()

    # --------------------------------
    # Helper
    # --------------------------------

    def get_checked_items(self):

        items = []

        for cb, text, score, _ in self.checks:

            if cb.isChecked():

                items.append(
                    (
                        text,
                        score
                    )
                )

        return items