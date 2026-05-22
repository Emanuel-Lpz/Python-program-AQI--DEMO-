def get_max_score(data):

    if data["type"] == "dropdown":

        return max(
            score
            for _, score
            in data["options"]
        )

    return sum(
        score
        for _, score
        in data["items"]
        if score > 0
    )


def check_auto_rejects(
    section_widgets,
    aqi
):

    errors = []

    for section, widgets in section_widgets.items():

        for criterion, widget in widgets.items():

            data = aqi[section][criterion]

            if data["type"] == "dropdown":

                if data.get("auto_reject"):

                    if widget.get_score() < get_max_score(data):

                        errors.append(
                            f"{section} → {criterion}"
                        )

            if data["type"] == "checklist":

                auto_items = data.get(
                    "auto_reject_items",
                    []
                )

                for cb, text, _ in widget.checks:

                    if text in auto_items:

                        if not cb.isChecked():

                            errors.append(
                                f"{section} → {criterion} → {text}"
                            )

    return errors


def generate_report(
    section_widgets,
    aqi
):

    total_score = 0

    section_lines = []

    for section, widgets in section_widgets.items():

        section_score = 0

        max_section_score = 0

        criterion_lines = []

        for criterion, widget in widgets.items():

            data = aqi[section][criterion]

            score = widget.get_score()

            max_score = get_max_score(data)

            section_score += score

            max_section_score += max_score

            criterion_lines.append(
                f"- {criterion}: {score}/{max_score}"
            )

        total_score += section_score

        block = (
            f"{section} "
            f"({section_score}/{max_section_score})\n"
            + "\n".join(criterion_lines)
        )

        section_lines.append(block)

    report = (
        f"AQI SCORE: {total_score}/100\n\n"
        + "\n\n".join(section_lines)
    )

    return report