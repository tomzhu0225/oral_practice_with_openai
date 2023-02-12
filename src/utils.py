import langcodes

def lang_to_code(language):
    if language == "Chinese":
        code = "zh-CN"
    elif language == "English":
        code = "en-US"
    elif language == "French":
        code = "fr-FR"
    elif language == "Japanese":
        code = "ja-JP"
    return code