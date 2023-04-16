from BonsaiBuddy.menus import MenuItem, MenuMixin

class AdminMenuMixin(MenuMixin):
    menu_context = {**MenuMixin.menu_context}
    menu_context["TreeInfo"][1].set_submenu([MenuItem("Create", "BonsaiAdmin:treeinfo_create")])

