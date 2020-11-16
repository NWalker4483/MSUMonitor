
def Clear(manager, cmd_str):
    num = len(manager.getStudentNames())
    names = manager.getStudentNames().copy()
    for name in names:
        manager.RemoveStudent(name)
    
    print(len(manager.getStudentNames()))
    return f"Removed all {num} students from the system"
cmd_set = {
    "clear": Clear
}