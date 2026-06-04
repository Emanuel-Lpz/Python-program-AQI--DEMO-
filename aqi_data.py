AQI = {

    "UNIQUE": {

        "Content Type": {
            "type": "dropdown",

            "description":
                "Fits the content definition of a Troubleshooting KB.",

            "auto_reject": True,

            "options": [
                ("Fits Troubleshooting KB definition", 5),
                ("Does not fit Troubleshooting KB definition", 0)
            ]
        },

        "Article Uniqueness": {
            "type": "dropdown",

            "description":
                "There are no duplicate articles internally or externally.",

            "auto_reject": True,

            "options": [
                ("No duplicates found", 5),
                ("Duplicate issue exists", 0)
            ]
        }
    },

    "GENERAL": {

        "Sections Filled Out": {
            "type": "dropdown",

            "description":
                "Title, Issue Details, and Solution are completed.",

            "auto_reject": True,

            "options": [
                ("All required sections completed", 1),
                ("Missing section(s)", 0)
            ]
        },

        "Competence": {
            "type": "dropdown",

            "description":
                "Correct grammar, spelling, and professional language.",

            "options": [
                ("Meets requirements", 2),
                ("Does not meet requirements", 0)
            ]
        },

        "Conventions": {
            "type": "dropdown",

            "description":
                "Follows KB style conventions.",

            "options": [
                ("Follows conventions", 1),
                ("Does not follow conventions", 0)
            ]
        },

        "Links": {
            "type": "checklist",

            "description":
                "Links evaluation.",

            "auto_reject_items": [
                "Correct destination and active"
            ],

            "items": [
                ("Links available", 1),
                ("Correct formatting", 1),
                ("Correct destination and active", 1)
            ]
        },

        "Images": {
            "type": "checklist",

            "description":
                "Images evaluation.",

            "auto_reject_items": [
                "Hosted correctly"
            ],

            "not_applicable": (
                "The KB does not include images",
                3
            ),
            "not_applicable_bold": False,

            "items": [
                ("Hosted correctly", 1),
                ("Appropriate to share", 2)
            ]
        }
    },

    "METADATA": {

        "Branding": {
            "type": "dropdown",

            "description":
                "Branding is correct.",

            "auto_reject": True,

            "options": [
                ("Correct branding", 1),
                ("Incorrect branding", 0)
            ]
        },

        "URL": {
            "type": "dropdown",

            "description":
                "URL matches title.",

            "auto_reject": True,

            "options": [
                ("Matches title", 1),
                ("Does not match title", 0)
            ]
        },

        "SEO Keywords": {
            "type": "checklist",

            "description":
                "SEO keyword evaluation.",

            "auto_reject_items": [
                "Minimum reached",
                "Comma separated"
            ],

            "items": [
                ("Relevant keywords", 1),
                ("Minimum reached", 1),
                ("Comma separated", 1)
            ]
        },

        "Internal Notes": {
            "type": "dropdown",

            "description":
                "Internal notes formatted correctly.",

            "options": [
                ("Correct formatting", 2),
                ("Incorrect formatting", 0)
            ]
        },

        "Validation Status": {
            "type": "checklist",

            "description":
                "Validation status evaluation.",

            "auto_reject_items": [
                "Correct status"
            ],

            "items": [
                ("Correct status", 3),
                ("Explanation included if needed", 2)
            ]
        },

        "Notes ID": {
            "type": "checklist",

            "description":
                "Populated if migrated.",

            "not_applicable": (
                "The KB was not migrated",
                1
            ),
            "not_applicable_bold": False,

            "items": [
                ("Populated", 1)
            ]
        },

        "Product Tags": {
            "type": "checklist",

            "description":
                "Product tagging evaluation.",

            "items": [
                ("Correct tagging", 1),
                ("Relevant tagging", 1)
            ]
        }
    },

    "TITLE": {

        "Correct Formatting": {
            "type": "dropdown",

            "description":
                "Correct KB title formatting.",

            "auto_reject": True,

            "options": [
                ("Correct formatting", 1),
                ("Incorrect formatting", 0)
            ]
        },

        "Related & Relevant": {
            "type": "checklist",

            "description":
                "Title quality evaluation.",

            "items": [
                ("Reflects issue discussed", 3),
                ("Sets expectations", 2),
                ("Searchable keywords", 3),
                ("Customer friendly terminology", 2),
                ("Title is a question", -1)
            ]
        },

        "NI Product Related": {
            "type": "dropdown",

            "description":
                "NI product referenced.",

            "options": [
                ("Product referenced", 2),
                ("Product not referenced", 0)
            ]
        },

        "Character Limit": {
            "type": "dropdown",

            "description":
                "75 characters or less preferred.",

            "options": [
                ("≤75 characters", 5),
                (">75 but justified", 3),
                (">75 not justified", 0)
            ]
        },

        "Capitalization": {
            "type": "dropdown",

            "description":
                "APA capitalization.",

            "options": [
                ("APA compliant", 2),
                ("Not APA compliant", 0)
            ]
        }
    },

    "ISSUE/CONTEXT": {

        "Other Sections/Tools": {
            "type": "checklist",

            "description":
                "Other sections and tools used correctly.",

            "conditional_items": {
                "The KB does not include attachments": [
                    "Attachments used correctly",
                    "Attachments referenced correctly"
                ]
            },

            "conditional_items_hidden_by_default": True,

            "items": [
                ("Other section used correctly", 1),
                ("Additional Information used correctly", 1),
                ("Relevant Related Links", 1),
                ("The KB does not include attachments", 2),
                ("Attachments used correctly", 1),
                ("Attachments referenced correctly", 1)
            ]
        },

        "Correct Formatting": {
            "type": "dropdown",

            "description":
                "Correct error formatting.",

            "options": [
                ("Correct formatting", 2),
                ("Incorrect formatting", 0)
            ]
        },

        "Overview of Scope": {
            "type": "dropdown",

            "description":
                "Issue should be clear quickly.",

            "options": [
                ("Complete overview", 4),
                ("Requires effort to understand", 2),
                ("Not discernible", 0)
            ]
        },

        "Action that Prompted": {
            "type": "dropdown",

            "description":
                "Context of occurrence is provided.",

            "options": [
                ("Complete context", 4),
                ("Partial context", 2),
                ("No context", 0)
            ]
        },

        "Environment Details": {
            "type": "dropdown",

            "description":
                "Relevant environmental details provided.",

            "options": [
                ("Complete details", 4),
                ("Partial details", 2),
                ("No details", 0)
            ]
        },

        "Symptoms": {
            "type": "checklist",

            "description":
                "Symptoms evaluation.",

            "items": [
                ("Clearly understandable", 3),
                ("Correct formatting (bulleted or not)", 1)
            ]
        },

        "Relevant Information": {
            "type": "dropdown",

            "description":
                "Only relevant information included.",

            "options": [
                ("Relevant only", 2),
                ("Includes unnecessary information", 0)
            ]
        }
    },

    "SOLUTION": {

        "Introduction / Expectations": {
            "type": "dropdown",

            "description":
                "Overview of why the issue occurs and what the solution accomplishes.",

            "options": [
                ("Complete overview", 3),
                ("Partial overview", 1),
                ("No overview", 0)
            ]
        },

        "Complete": {
            "type": "dropdown",

            "description":
                "Completeness of the solution.",

            "options": [
                ("No additional information needed", 8),
                ("Some information missing", 5),
                ("Significant information missing", 2),
                ("Incomplete solution", 0)
            ]
        },

        "Relevant & Concise": {
            "type": "dropdown",

            "description":
                "Appropriate level of detail.",

            "options": [
                ("Just enough information", 4),
                ("Too much information", 0)
            ]
        },

        "Formatting": {
            "type": "checklist",

            "description":
                "Solution formatting evaluation.",

            "items": [
                ("Bullets/Numbers used appropriately", 2),
                ("Correct ordering", 2),
                ("Predetermined text used", 1),
                ("Wall of text", -2)
            ]
        }
    }
}