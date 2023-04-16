from BonsaiBuddy.menus import MenuItem, MenuMixin

class BonsaiAdviceMenuMixin(MenuMixin):
    menu_context = {"menu_items": [
        MenuItem("TreeInfo", "TreeInfo:index"),
        MenuItem("Advices", "BonsaiAdvice:index"),
        MenuItem("Admin", "BonsaiAdmin:index", permission="TreeInfo.change_content"),
    ]}
