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
        self.conditional_items = data.get("conditional_items", {})
        self.checkbox_map = {}

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

        if self.not_applicable_data:
            na_label, na_score = self.not_applicable_data
            self.not_applicable_checkbox = QCheckBox(
                f"{na_label} ({na_score:+d})"
            )
            if self.data.get("not_applicable_bold", True):
                self.not_applicable_checkbox.setStyleSheet(
                    "font-weight:bold;"
                )
            self.not_applicable_checkbox.toggled.connect(
                self.on_not_applicable_toggled
            )
            layout.addWidget(self.not_applicable_checkbox)

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

            style = ""

            if self.not_applicable_data:
                style += "margin-left:18px;"

            if any(
                text in children
                for children in self.conditional_items.values()
            ):
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
                    score
                )
            )

            self.checkbox_map[text] = cb

            if text in self.conditional_items:
                cb.stateChanged.connect(
                    lambda checked, trigger=text: self.on_conditional_trigger_toggled(
                        trigger,
                        checked
                    )
                )

    # --------------------------------
    # Score
    # --------------------------------

    def get_score(self):

        if self.is_not_applicable():
            return self.not_applicable_data[1]

        score = 0

        for cb, _, points in self.checks:

            if cb.isChecked():
                score += points

        return max(score, 0)

    def get_max_score(self):

        if self.is_not_applicable():
            return self.not_applicable_data[1]

        return sum(
            score
            for cb, _, score in self.checks
            if score > 0 and cb.isVisible()
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
            for cb, _, _
            in self.checks
        )

    def on_not_applicable_toggled(self, checked):

        for cb, _, _ in self.checks:
            cb.setVisible(not checked)
            if checked:
                cb.setChecked(False)

        self.noteChanged.emit()

    def on_conditional_trigger_toggled(
        self,
        trigger_text,
        checked
    ):

        controlled_items = self.conditional_items.get(
            trigger_text,
            []
        )

        for item_text in controlled_items:
            cb = self.checkbox_map.get(item_text)
            if cb is None:
                continue

            cb.setVisible(not checked)
            if checked:
                cb.setChecked(False)

        self.noteChanged.emit()

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