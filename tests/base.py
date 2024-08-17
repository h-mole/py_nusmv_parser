import os


def get_asset_path(path):
    """
    Returns the absolute path to the given path in the assets folder.
    """
    print("__file__", __file__)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("root", root)
    return os.path.join(root, "assets", path)
