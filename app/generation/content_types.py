"""
Per-format templates/guidance for different content types.
"""

CONTENT_TYPES = {
    "email": {
        "guidance": (
            "Standard email structure: greeting, body, sign-off. "
            "Keep it appropriately concise unless the style profile favors longer prose."
        ),
    },
    "linkedin_post": {
        "guidance": (
            "Short paragraphs or line breaks for readability, hook in the first line, "
            "no email-style greeting/sign-off. Match the user's typical emoji/hashtag use."
        ),
    },
    "blog_post": {
        "guidance": (
            "Longer-form, may include headers/sections. Should read as a complete piece, "
            "not a fragment."
        ),
    },
    "message": {
        "guidance": (
            "Casual, short-form (Slack/text message style). No formal greeting or sign-off "
            "unless the style profile indicates the user uses one."
        ),
    },
}