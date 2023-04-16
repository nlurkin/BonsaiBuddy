from BonsaiBuddy.menus import MenuItem, MenuMixin

class BonsaiAdviceMenuMixin(MenuMixin):
    menu_context = {**MenuMixin.menu_context}
