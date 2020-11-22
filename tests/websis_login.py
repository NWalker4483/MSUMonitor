import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import utils.websis as wb
from student import Student
import auth 
ret, sess = wb.LoginToWebsis(Student(auth.username, auth.password))
if ret:
    try: 
        wb.get_options_for(sess, "202070","MATH", "241")
    except Exception as e:
        print("Test Failed")
        raise(e)
    print("Test Passed")