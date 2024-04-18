for pv[get_pid()]["f"] in [
    "mkuart.lja",
    "mkuart.py",
    "rmuart.lja",
    "rmuart.py",
    "terminal.lja",
    "terminal.py",
]:
    be.based.run("cp " + vr("f") + " /bin/" + vr("f"))
be.based.run("cp mkuart.txt /usr/share/help/mkuart.txt")

be.api.setvar("return", "0")
