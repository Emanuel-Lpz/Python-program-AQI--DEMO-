from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


class DropdownWidget(QWidget):

    def __init__(self, title, data):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>{title}</b>"))

        self.combo = QComboBox()

        for text, score in data["options"]:
            self.combo.addItem(text, score)

        layout.addWidget(self.combo)

        desc = QLabel(data["description"])
        desc.setWordWrap(True)

        layout.addWidget(desc)

    def get_score(self):
        return self.combo.currentData()


class ChecklistWidget(QWidget):

    def __init__(self, title, data):
        super().__init__()

        self.checks = []

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"<b>{title}</b>"))

        desc = QLabel(data["description"])
        desc.setWordWrap(True)

        layout.addWidget(desc)

        for text, score in data["items"]:

            cb = QCheckBox(
                f"{text} ({score:+d})"
            )

            layout.addWidget(cb)

            self.checks.append((cb, score))

    def get_score(self):

        score = 0

        for cb, points in self.checks:
            if cb.isChecked():
                score += points

        return max(score, 0)