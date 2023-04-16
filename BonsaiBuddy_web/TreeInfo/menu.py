from BonsaiBuddy.menus import MenuItem, MenuMixin

class TreeInfoMenuMixin(MenuMixin):
    menu_context = {**MenuMixin.menu_context}
