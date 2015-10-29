import datetime
from markupsafe import Markup


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


def jinja2_filter_date_with_delta(date, delta=1):
    return date + datetime.timedelta(delta)


def jinja2_filter_startswith(string, start_str):
    return (string is not None) and (string.startswith(start_str))


def jinja2_filter_photo_collection_heat_map(collections):
    styles, categories = dict(), dict()
    result = ''
    for c in collections:
        if c.style is not None:
            if styles.has_key(c.style.display):
                styles[c.style.display] += 1
            else:
                styles[c.style.display] = 1
        if c.category is not None:
            if categories.has_key(c.category.display):
                categories[c.category.display] += 1
            else:
                categories[c.category.display] = 1
    if len(styles) > 0:
        for k, v in styles.iteritems():
            result = result + '<span class="styles-categories">' + k + ':' + str(v) + '</span>'
    if len(categories) > 0:
        for k, v in categories.iteritems():
            result = result + '<span class="styles-categories">' + k + ':' + str(v) + '</span>'
    return Markup(result)
