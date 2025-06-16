import unittest
import functions.get_files_info as gfi
import functions.get_file_content as gf
import functions.write_file as wf
import functions.run_python as rf

class MainTests(unittest.TestCase):

    def test_run_file_main(self):
        run_file = rf.run_python_file("calculator", "calculator/main.py")
        print(run_file)
    
    def test_run_file_test(self):
        run_file = rf.run_python_file("calculator", "calculator/tests.py")
        print(run_file)
    
    def test_run_file_bw(self):
        run_file = rf.run_python_file("calculator", "../main.py")
        print(run_file)

    def test_run_file_nonexist(self):
        run_file = rf.run_python_file("calculator", "calculator/nonexistent.py")
        print(run_file)


if __name__ == '__main__':
    unittest.main()