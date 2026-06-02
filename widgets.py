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


class ChecklistWidget(QWidget):

    noteChanged = Signal()

    def __init__(self, title, data):

        super().__init__()

        self.title = title
        self.data = data
        self.note = None

        self.checks = []

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

        for text, score in data["items"]:

            display_text = text

            if text in auto_items:
                display_text = text

            cb = QCheckBox(
                f"{display_text} ({score:+d})"
            )

            if text in auto_items:

                cb.setStyleSheet(
                    f"color:{AUTO_REJECT_COLOR};"
                )

                cb.setToolTip(
                    "AUTO-REJECT item.\n\n"
                    "If this checkbox is not satisfied "
                    "the KB must be rejected."
                )

            layout.addWidget(cb)

            self.checks.append(
                (
                    cb,
                    text,
                    score
                )
            )

    # --------------------------------
    # Score
    # --------------------------------

    def get_score(self):

        score = 0

        for cb, _, points in self.checks:

            if cb.isChecked():
                score += points

        return max(score, 0)

    def get_max_score(self):

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

    def is_complete(self):

        return any(
            cb.isChecked()
            for cb, _, _
            in self.checks
        )

    # --------------------------------
    # Helper
    # --------------------------------

    def get_checked_items(self):

        items = []

        for cb, text, score in self.checks:

            if cb.isChecked():

                items.append(
                    (
                        text,
                        score
                    )
                )

        return items