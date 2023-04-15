from BonsaiBuddy.menus import MenuItem, MenuMixin

class AdminMenuMixin(MenuMixin):
    menu_context = {"menu_items": [
        MenuItem("Admin", "BonsaiAdmin:index"),
        MenuItem("TreeInfo", submenu=[
            MenuItem("Create", "BonsaiAdmin:treeinfo_create")
        ])
    ]}
