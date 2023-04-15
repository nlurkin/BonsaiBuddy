class MenuItem(object):
    def __init__(self, display, urlref=None, submenu=None):
        if submenu:
            self.itype = "submenu"
        else:
            self. itype = "menuitem"
        self. urlref = urlref
        self. display = display
        self. submenu = submenu

class MenuMixin(object):
    menu_context = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.menu_context)
        return context