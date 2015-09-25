def jinja2_filter_substring(string, direction="left", length='100'):
    if string is None:
        return ''
    if direction == "left":
        if length >= len(string):
            return string
        return string[0:length]
    elif direction == "right":
        if length >= len(string):
            return ''
        return string[length:len(string)]


def jinja2_filter_startswith(string, start_str):
    return (string is not None) and (string.startswith(start_str))
