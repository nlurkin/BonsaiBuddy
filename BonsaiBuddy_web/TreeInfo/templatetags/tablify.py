import django.utils.safestring as safestring
from django import template

register = template.Library()


def tablify(array, has_header=False):
    header = ""
    body = ""
    if has_header and len(array) > 0:
        header = "<tr>" + \
            "".join([f"<th>{_}</th>" for _ in array[0]]) + "</tr>"
        print(header)
        array = array[1:]
    body = "".join(["<tr>" + f"<th>{row[0]}</th>" + "".join(
        [f"<td>{_}</td>" for _ in row[1:]]) + "</tr>" for row in array])
    return safestring.mark_safe(f"<table class='table table-striped'>{header}{body}</table>".replace("\n", "</br>"))


register.filter("tablify", tablify)
