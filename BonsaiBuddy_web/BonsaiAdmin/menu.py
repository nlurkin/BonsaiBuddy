from BonsaiBuddy.menus import MenuItem, MenuMixin
import copy

class AdminMenuMixin(MenuMixin):
    menu_context = MenuMixin.get_init_menu_context()
    menu_context["TreeInfo"][1].set_submenu([MenuItem("Create", "BonsaiAdmin:treeinfo_create")])
    menu_context["Advices"][1].set_submenu([MenuItem("Create technique", "BonsaiAdmin:technique_create"),
                                            MenuItem("Create objective", "BonsaiAdmin:objective_create")])

