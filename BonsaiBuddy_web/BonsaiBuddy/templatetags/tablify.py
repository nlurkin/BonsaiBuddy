import django.utils.safestring as safestring
from django import template

register = template.Library()


def tablify(array, has_header=False):
    header = ""
    body = ""
    ncols = max(len(r) for r in array)
    if has_header and len(array) > 0:
        header = "<tr>" + \
            "".join([f"<th scope='col'>{_}</th>" for _ in array[0]]) + "</tr>"
        array = array[1:]

    for row in array:
        span = "" if len(row)==ncols else f"colspan='{ncols-len(row)+1}'"
        body += "<tr>" + f"<th scope='row' {span}>{row[0]}</th>" + "".join([f"<td>{_}</td>" for _ in row[1:]]) + "</tr>"
    return safestring.mark_safe(f"<table class='table table-striped'>{header}{body}</table>".replace("\n", "</br>"))


register.filter("tablify", tablify)
