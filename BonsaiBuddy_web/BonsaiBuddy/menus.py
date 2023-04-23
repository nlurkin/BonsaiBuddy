import copy

class MenuItem(object):
    def __init__(self, display, urlref=None, submenu=None, permission=None):
        if submenu:
            self.itype = "submenu"
        else:
            self.itype = "menuitem"
        self._urlref = urlref
        self._display = display
        self.submenu = submenu
        self.permission = permission

    def set_submenu(self, submenu):
        self.itype = "submenu"
        self.submenu = submenu

    def is_authenticated(self, status):
        return self

    @property
    def display(self):
        return self._display

    @property
    def urlref(self):
        return self._urlref

class LoginMenuItem(MenuItem):
    def __init__(self):
        super().__init__("Login", "login")

    def is_authenticated(self, status):
        if status:
            self._display = "Logout"
            self._urlref = "logout"
        else:
            self._display = "Login"
            self._urlref = "login"
        return self

    @property
    def display(self):
        return self._display

    @property
    def urlref(self):
        return self._urlref

class MenuMixin(object):
    menu_context = {
        "TreeInfo": (0, MenuItem("TreeInfo", "TreeInfo:index")),
        "Advices": (1, MenuItem("Advices", "BonsaiAdvice:index")),
        "Admin": (2, MenuItem("Admin", "BonsaiAdmin:index", permission="TreeInfo.change_content")),
        "Login": (3, LoginMenuItem()),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.build_menu_context(self.request))
        return context

    def build_menu_context(self, request):
        auth_status = request.user.is_authenticated
        return {"menu_items": [v[1].is_authenticated(auth_status) for v in sorted(self.menu_context.values(), key=lambda x: x[0])]}

    @staticmethod
    def get_init_menu_context():
        return {**copy.deepcopy(MenuMixin.menu_context)}