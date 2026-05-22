def get_section_score(section_widgets):

    total = 0

    for widget in section_widgets.values():
        total += widget.get_score()

    return total