from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QCheckBox
)

AUTO_REJECT_COLOR = "#00AD7C"


class DropdownWidget(QWidget):

    def __init__(self, title, data):

        super().__init__()

        self.data = data

        layout = QVBoxLayout(self)

        # ----------------------------
        # Title
        # ----------------------------

        title_text = title

        if data.get("auto_reject"):
            title_text += " *"

        title_label = QLabel(
            f"<b>{title_text}</b>"
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

    def __init__(self, title, data):

        super().__init__()

        self.data = data

        self.checks = []

        layout = QVBoxLayout(self)

        # ----------------------------
        # Title
        # ----------------------------

        title_text = title

        if data.get(
            "auto_reject_items"
        ):
            title_text += " *"

        title_label = QLabel(
            f"<b>{title_text}</b>"
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
                display_text += "*"

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