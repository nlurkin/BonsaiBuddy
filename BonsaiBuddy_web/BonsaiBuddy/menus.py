import copy
from utils import user_has_any_perms

class MenuItem(object):
    def __init__(self, display, urlref=None, submenu=None, permissions=None, requires_auth=False):
        if submenu:
            self.itype = "submenu"
        else:
            self.itype = "menuitem"
        self._urlref = urlref
        self._display = display
        self.submenu = submenu
        self.permissions = [permissions] if isinstance(permissions, str) else permissions
        self.current_user = None
        self.requires_auth = requires_auth

    def set_submenu(self, submenu):
        self.itype = "submenu"
        self.submenu = submenu

    def set_user(self, user):
        self.current_user = user
        if self.submenu:
            for subitem in self.submenu:
                subitem.set_user(user)
        return self

    def is_displayable(self):
        auth_ok = False
        perms_ok = False
        if self.permissions is None or user_has_any_perms(self.current_user, self.permissions):
            perms_ok = True
        if not self.requires_auth or self.current_user.is_authenticated:
            auth_ok = True
        return perms_ok and auth_ok

    def display(self):
        return self._display

    def urlref(self):
        return self._urlref

class LoginMenuItem(MenuItem):
    def __init__(self):
        super().__init__("Login", "login")

    def display(self):
        if self.current_user and self.current_user.is_authenticated:
            return "Logout"
        else:
            return "Login"

    def urlref(self):
        if self.current_user and self.current_user.is_authenticated:
            return "logout"
        else:
            return "login"

class MenuMixin(object):
    menu_context = {
        "TreeInfo": (0, MenuItem("TreeInfo", "TreeInfo:index")),
        "Advices":  (1, MenuItem("Advices", "BonsaiAdvice:index")),
        "Profile":  (2, MenuItem("Profile", "Profile:detail", requires_auth=True)),
        "MyTrees":  (3, MenuItem("My Trees", "Profile:my_trees", requires_auth=True)),
        "Admin":    (4, MenuItem("Admin", "BonsaiAdmin:index", permissions=["BonsaiAdvice.change_content", "TreeInfo.change_content"])),
        "Login":    (5, LoginMenuItem()),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.build_menu_context(self.request))
        return context

    def build_menu_context(self, request):
        return {"menu_items": [v[1].set_user(request.user) for v in sorted(self.menu_context.values(), key=lambda x: x[0])]}

    @staticmethod
    def get_init_menu_context():
        return {**copy.deepcopy(MenuMixin.menu_context)}