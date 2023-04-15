class MenuItem(object):
    def __init__(self, display, urlref=None, submenu=None):
        if submenu:
            self.itype = "submenu"
        else:
            self. itype = "menuitem"
        self. urlref = urlref
        self. display = display
        self. submenu = submenu