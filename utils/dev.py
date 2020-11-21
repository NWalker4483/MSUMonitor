
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
    
def Check(manager, cmd_str):
    try:
        return str("")
    except:
        return str("")
cmd_set = {
    "clear": Clear,
    "list": List,
    "check": Check
}