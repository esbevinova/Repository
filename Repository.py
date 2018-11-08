import unittest
from HW09ebevinova import Student, Instructor, Repository

class CommonTest(unittest.TestCase):
    
    directory = r'C:\Users\Kat\Documents\VSC-Python\810\test'

    def test_student(self):
        stevens = Repository(r'C:\Users\Kat\Documents\VSC-Python\810\test')
        student_details = [s.pt_row() for s in stevens.students.values()]
        expect = [['10103', 'Baldwin, C', 'SFEN', {'SSW 564', 'SSW 687', 'CS 501', 'SSW 567'}, {'SSW 555', 'SSW 540'}, None]] 
        self.assertEqual (student_details, expect)

    def test_instructor(self):
        stevens = Repository(r'C:\Users\Kat\Documents\VSC-Python\810\test')
        instructor_details = [row for instructor in stevens.instructors.values() for row in instructor.pt_row()]
        expect = [['98765',	'Einstein, A', 'SFEN', 'SSW 567', 1]]
        self.assertEqual (instructor_details, expect)    
    
    def test_majors(self):
        stevens = Repository(r'C:\Users\Kat\Documents\VSC-Python\810\test')
        majors_details = {m.pt_row() for m in stevens.majors.values()}
        expect = [['SFEN', {'SSW 564', 'SSW 555', 'SSW 567', 'SSW 540'}, {'CS 513', 'CS 501', 'CS 545'}],
                  ['SYEN', {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 810', 'SSW 565', 'SSW 540'}]] 
        self.assertEqual (majors_details, expect)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)