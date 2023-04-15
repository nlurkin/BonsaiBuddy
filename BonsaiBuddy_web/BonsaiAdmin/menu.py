from BonsaiBuddy.menus import MenuItem

menu_context = {"menu_items": [
    MenuItem("Admin", "BonsaiAdmin:index"),
    MenuItem("TreeInfo", submenu=[
        MenuItem("Create", "BonsaiAdmin:treeinfo_create")
    ])
]}
