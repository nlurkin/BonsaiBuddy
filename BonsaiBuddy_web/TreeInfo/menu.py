from BonsaiBuddy.menus import MenuItem, MenuMixin

class TreeInfoMenuMixin(MenuMixin):
    menu_context = {"menu_items": [
        MenuItem("TreeInfo", "TreeInfo:index"),
        MenuItem("Admin", "BonsaiAdmin:index", permission="TreeInfo.change_content"),
    ]}
