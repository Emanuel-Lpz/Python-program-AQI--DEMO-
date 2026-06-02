def get_max_score(data):
    """
    Returns the maximum obtainable score
    for a criterion.
    """

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


# --------------------------------------------------
# AUTO REJECT CHECKS
# --------------------------------------------------

def check_auto_rejects(
    section_widgets,
    aqi
):
    """
    Returns a list of all auto-reject failures.
    """

    errors = []

    for section, widgets in section_widgets.items():

        for criterion, widget in widgets.items():

            data = aqi[section][criterion]

            # ----------------------------------
            # Dropdown auto reject
            # ----------------------------------

            if (
                data["type"] == "dropdown"
                and data.get("auto_reject")
            ):

                current_score = widget.get_score()

                max_score = get_max_score(
                    data
                )

                if current_score < max_score:

                    errors.append(
                        f"{section} → {criterion}"
                    )

            # ----------------------------------
            # Checklist auto reject
            # ----------------------------------

            if (
                data["type"] == "checklist"
                and data.get(
                    "auto_reject_items"
                )
            ):

                if getattr(widget, "is_not_applicable", lambda: False)():
                    continue

                auto_items = data[
                    "auto_reject_items"
                ]

                for (
                    cb,
                    text,
                    _
                ) in widget.checks:

                    if (
                        text in auto_items
                        and not cb.isChecked()
                    ):

                        errors.append(
                            f"{section} → "
                            f"{criterion} → "
                            f"{text}"
                        )

    return errors


# --------------------------------------------------
# SECTION SCORE
# --------------------------------------------------

def get_section_score(
    widgets
):
    score = 0

    for widget in widgets.values():

        score += widget.get_score()

    return score


# --------------------------------------------------
# SECTION MAX SCORE
# --------------------------------------------------

def get_section_max_score(
    section_name,
    aqi
):
    total = 0

    for criterion_data in aqi[
        section_name
    ].values():

        total += get_max_score(
            criterion_data
        )

    return total


# --------------------------------------------------
# TOTAL SCORE
# --------------------------------------------------

def get_total_score(
    section_widgets
):
    total = 0

    for widgets in section_widgets.values():

        total += get_section_score(
            widgets
        )

    return total


# --------------------------------------------------
# REPORT
# --------------------------------------------------

def generate_report(
    section_widgets,
    aqi
):
    """
    Generates the detailed
    clipboard report.
    """

    total_score = 0

    report_lines = []

    # ----------------------------------
    # Calculate total
    # ----------------------------------

    for widgets in section_widgets.values():

        total_score += get_section_score(
            widgets
        )

    report_lines.append(
        f"AQI SCORE: {total_score}/100"
    )

    report_lines.append("")

    # ----------------------------------
    # Section details
    # ----------------------------------

    for (
        section_name,
        widgets
    ) in section_widgets.items():

        section_score = 0

        section_max = 0

        for (
            criterion,
            widget
        ) in widgets.items():

            criterion_data = aqi[
                section_name
            ][criterion]

            score = widget.get_score()

            max_score = get_max_score(
                criterion_data
            )

            section_score += score

            section_max += max_score

        report_lines.append(
            f"{section_name} "
            f"({section_score}/{section_max})"
        )

        # --------------------------
        # Criterion details
        # --------------------------

        for (
            criterion,
            widget
        ) in widgets.items():

            criterion_data = aqi[
                section_name
            ][criterion]

            score = widget.get_score()

            max_score = get_max_score(
                criterion_data
            )

            report_lines.append(
                f"- {criterion}: "
                f"{score}/{max_score}"
            )

        report_lines.append("")

    note_lines = []

    for widgets in section_widgets.values():
        for widget in widgets.values():
            if hasattr(widget, "get_note_lines"):
                note_lines.extend(
                    widget.get_note_lines()
                )

    if note_lines:
        report_lines.append("")
        report_lines.extend(note_lines)

    return "\n".join(
        report_lines
    )


# --------------------------------------------------
# DASHBOARD SUMMARY
# --------------------------------------------------

def generate_dashboard(
    section_widgets,
    aqi
):
    """
    Generates the compact
    score panel shown in UI.
    """

    lines = []

    total_score = 0

    total_max = 0

    for (
        section_name,
        widgets
    ) in section_widgets.items():

        section_score = get_section_score(
            widgets
        )

        section_max = (
            get_section_max_score(
                section_name,
                aqi
            )
        )

        total_score += section_score

        total_max += section_max

        lines.append(
            f"{section_name:<15}"
            f"{section_score}/{section_max}"
        )

    lines.append("")
    lines.append(
        f"TOTAL SCORE: "
        f"{total_score}/{total_max}"
    )

    return "\n".join(
        lines
    )