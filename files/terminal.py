rename_process("terminal")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if "help" in vr("opts")["o"] or "-h" in vr("opts")["o"] or not vr("opts")["w"]:
    term.write("Usage: terminal [get/list/activate] [ttyXXXX]")
else:
    vr("0", vr("opts")["w"][0])
    if vr("0") == "get":
        be.api.setvar("return", pv[0]["console_active"])
    elif vr("0") == "activate":
        if len(vr("opts")["w"]) - 1:
            vr("1", vr("opts")["w"][1])
            if vr("1") in pv[0]["consoles"]:
                term.console = pv[0]["consoles"][vr("1")]
                pv[0]["console_active"] = vr("1")
                be.api.setvar("return", "0")
            else:
                term.write("Console not found.")
        else:
            term.write("No console specified!")
    elif vr("0") == "list":
        for pv[get_pid()]["i"] in pv[0]["consoles"].keys():
            term.nwrite(vr("i"))
            if vr("i") == pv[0]["console_active"]:
                term.write(" [ACTIVE]")
            else:
                term.write()
        be.api.setvar("return", "0")
    elif vr("0") == "connect":
        if len(vr("opts")["w"]) - 1:
            vr("1", vr("opts")["w"][1])
            if vr("1") in pv[0]["consoles"]:
                vr("con", pv[0]["consoles"][vr("1")])
                be.api.setvar("return", "0")

                vr("cont", True)
                vr("held", 0)
                vr("held_st", None)
                term.write("To disconnect, hold down Ctrl-Q.\n" + "-" * 32)
                while vr("cont"):
                    be.io.ledset(1)
                    try:
                        while vr("cont"):
                            try:
                                vr("dat", term.console.read(term.console.in_waiting))
                                if vr("dat"):
                                    if b"\n" in vr("dat"):
                                        vr("dat", vr("dat").replace(b"\n", b"\r"))
                                    be.io.ledset(3)
                                    vr("datl", list(vr("dat")))
                                    vr("17c", vr("datl").count(17))
                                    if vr("17c") == len(vr("datl")):
                                        if not vr("held"):
                                            vrp("held", vr("17c"))
                                            vr("held_st", time.monotonic())
                                        elif vr("held") > 9:
                                            vr("cont", False)
                                            term.write(
                                                "\n" + "-" * 32 + "\nRelease to quit."
                                            )
                                            while True:
                                                time.sleep(0.3)
                                                if term.console.in_waiting:
                                                    term.console.read(
                                                        term.console.in_waiting
                                                    )
                                                else:
                                                    break
                                        else:
                                            vr("held_st", time.monotonic())
                                            vrp("held")
                                    else:
                                        if vr("held"):
                                            vr("held", 0)
                                            vr("con").write(b"\x11")
                                        vr("con").write(vr("dat"))
                                    be.io.ledset(1)
                                elif (
                                    vr("held")
                                    and time.monotonic() - vr("held_st") > 1
                                ):
                                    vr("held", 0)
                                    vr("con").write(b"\x11")
                                vr("dat", vr("con").read(vr("con").in_waiting))
                                if vr("dat"):
                                    term.console.write(vr("dat"))
                            except KeyboardInterrupt:
                                be.io.ledset(3)
                                vr("con").write(b"\x03")
                                be.io.ledset(1)
                    except KeyboardInterrupt:
                        vr("con").write(b"\x03")
            else:
                term.write("Console not found.")
        else:
            term.write("No console specified!")
    else:
        term.write("Unknown option specified, try running `terminal --help`")
