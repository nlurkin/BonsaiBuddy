import copy

class MenuItem(object):
    def __init__(self, display, urlref=None, submenu=None, permission=None):
        if submenu:
            self.itype = "submenu"
        else:
            self.itype = "menuitem"
        self.urlref = urlref
        self.display = display
        self.submenu = submenu
        self.permission = permission

    def set_submenu(self, submenu):
        self.itype = "submenu"
        self.submenu = submenu

class MenuMixin(object):
    menu_context = {
        "TreeInfo": (0, MenuItem("TreeInfo", "TreeInfo:index")),
        "Advices": (1, MenuItem("Advices", "BonsaiAdvice:index")),
        "Admin": (2, MenuItem("Admin", "BonsaiAdmin:index", permission="TreeInfo.change_content")),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.build_menu_context())
        return context

    def build_menu_context(self):
        return {"menu_items": [v[1] for v in sorted(self.menu_context.values(), key=lambda x: x[0])]}

    @staticmethod
    def get_init_menu_context():
        return {**copy.deepcopy(MenuMixin.menu_context)}