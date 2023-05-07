from django import forms
from django.utils.safestring import mark_safe

def python_to_js(pydict):
    if isinstance(pydict, dict):
        return ", ".join([f"{k}: {{{python_to_js(v)}}}" if isinstance(v, dict) else f"{k}: {python_to_js(v)}" for k, v in pydict.items()]) + ", "
    elif isinstance(pydict, str):
        if pydict == "Infinity":
            return pydict
        return f"'{pydict}'"
    elif isinstance(pydict, bool):
        return str(pydict).lower()
    return f"{pydict}"

class TagifyWidget(forms.SelectMultiple):
    class Media:
        js = ('https://cdn.jsdelivr.net/npm/@yaireo/tagify', 'https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.polyfills.min.js',)
        css = {"all": ('https://cdn.jsdelivr.net/npm/@yaireo/tagify/dist/tagify.css',)}

    template_name = "widgets/selecttags.html"

    def __init__(self, *args, **kwargs):
        self.minCharForSuggestions = kwargs.pop("minCharForSuggestions", 0)
        self.closeOnSelect = kwargs.pop("closeOnSelect", False)
        self.maxItems = kwargs.pop("maxItems", 20)
        self.maxTags = kwargs.pop("maxTags", "Infinity")
        self.enforceList = kwargs.pop("enforceList", True)
        self.editable = kwargs.pop("editable", False)
        super().__init__(*args, **kwargs)

    def build_dropdown_params(self):
        return {"enabled": self.minCharForSuggestions,
                "closeOnSelect": self.closeOnSelect,
                "maxItems": self.maxItems,
                "mapValueTo": "name",
                }

    def build_generic_params(self):
        return {"editTags": False if self.enforceList else self.editable, # No sense to make the tags editable if the use has no choice anyways
                "enforceWhitelist": self.enforceList,
                "tagTextProp": "name",
                "maxTags": self.maxTags,
                }

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["tagify"] = mark_safe(python_to_js({**self.build_generic_params(), "dropdown": self.build_dropdown_params()}))
        return context