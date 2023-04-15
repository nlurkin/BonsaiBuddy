from BonsaiBuddy.menus import MenuItem, MenuMixin

class TreeInfoMenuMixin(MenuMixin):
    menu_context = {"menu_items": [
        MenuItem("TreeInfo", "TreeInfo:index"),
    ]}
