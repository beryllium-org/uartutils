for i in [
    "mkuart.lja",
    "mkuart.py",
    "rmuart.lja",
    "rmuart.py",
    "terminal.lja",
    "terminal.py",
]:
    shutil.copy(i, path.join(root, "bin", i))

shutil.copy("mkuart.txt", path.join(root, "usr/share/help", "mkuart.txt"))
