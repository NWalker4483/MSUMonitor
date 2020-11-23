from student import Student
from manager import Manager
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
manager = Manager()
student = Student("niwal7", None)
manager.AddStudent(student)
manager.AddCourseSubscribtion("202070", "TEST", "101", "111111", "niwal7")
for i in range(4):  # Subscriptions should be removed after four tries
    manager.CheckCourseAvailability()
    print(f"Check {i}")
if (len(student.getNeededCourses()) == 0):
    print("Test Passed")
else:
    print("Test Failed")
