from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


class DropdownWidget(QWidget):

    def __init__(self, title, data):

        super().__init__()

        self.data = data

        layout = QVBoxLayout(self)

        title_label = QLabel(f"<b>{title}</b>")

        layout.addWidget(title_label)

        self.combo = QComboBox()

        self.combo.addItem(
            "-- Select an option --",
            None
        )

        for text, score in data["options"]:

            display = f"{text} ({score:+d})"

            self.combo.addItem(
                display,
                score
            )

        self.combo.setCurrentIndex(0)

        layout.addWidget(self.combo)

        desc = QLabel(
            data["description"]
        )

        desc.setWordWrap(True)

        layout.addWidget(desc)

    def get_score(self):

        value = self.combo.currentData()

        if value is None:
            return 0

        return value

    def is_complete(self):

        return self.combo.currentData() is not None


class ChecklistWidget(QWidget):

    def __init__(self, title, data):

        super().__init__()

        self.data = data

        self.checks = []

        layout = QVBoxLayout(self)

        title_label = QLabel(f"<b>{title}</b>")

        layout.addWidget(title_label)

        desc = QLabel(
            data["description"]
        )

        desc.setWordWrap(True)

        layout.addWidget(desc)

        for text, score in data["items"]:

            cb = QCheckBox(
                f"{text} ({score:+d})"
            )

            layout.addWidget(cb)

            self.checks.append(
                (cb, text, score)
            )

    def get_score(self):

        score = 0

        for cb, _, points in self.checks:

            if cb.isChecked():
                score += points

        return max(score, 0)

    def is_complete(self):

        return any(
            cb.isChecked()
            for cb, _, _ in self.checks
        )