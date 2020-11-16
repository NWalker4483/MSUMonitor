
def Clear(manager, cmd_str):
    print(len(manager.getStudentNames()))
    names = manager.getStudentNames().copy()
    for name in names:
        manager.RemoveStudent(name)
    
    print(len(manager.getStudentNames()))
cmd_set = {
    "clear": Clear
}