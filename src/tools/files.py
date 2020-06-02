from pathlib import Path
from tools.copytree import copytree


def ensure_directory(path):
    Path("../out/news").mkdir(parents=True, exist_ok=True)


def copy_tree(src, dst, symlinks=False, ignore=None):
    return copytree(src, dst, symlinks, ignore)


def read_all_text(path):
    with open(path, "r") as f:
        return f.read()
