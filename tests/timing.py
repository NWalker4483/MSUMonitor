import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from manager import Manager
from student import Student
manager = Manager()
student = Student("testuser", None)
manager.AddStudent(student)
manager.AddCourseSubscribtion("202070","MATH","241","111111","testuser")
for i in range(4): # Subscriptions should be removed after four tries
    manager.CheckCourseAvailability()  
    print(f"Check {i}")
if (len(student.getNeededCourses())==0):
    print("Test Passed")
else:
    print("Test Failed")