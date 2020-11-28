# A set of tools that the devs can access through the frontend
import logging

log = logging.getLogger("AutoRegistration.sub")


def Clear(manager, cmd_str):
    names = manager.getStudentNames().copy()
    num = len(names)
    for name in names:
        manager.RemoveStudent(name)
    return f"Removed all {num} students from the system"


def List(manager, cmd_str):
    return str(manager.getStudentNames())


def Kill(manager, cmd_str):
    exit()


def Remove(manager, cmd_str):
    manager.RemoveStudent(cmd_str.strip())
    return f"Removed {cmd_str}"


cmd_set = {
    "clear": Clear,
    "list": List,
    "remove": Remove,
    "kill": Kill
}
