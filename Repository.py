"""SSW-810-A
   Ekaterina (katya) Bevinova
   HW09
"""
from prettytable import PrettyTable
from HW08ebevinova import read_file
import unittest
import os
from collections import defaultdict



class Student:
    "A class that stores all the information about students."
    pt_hdr = ['CWID', 'Name', 'Completed Courses']
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict() #key is course, value is grade (we're not using defaultdict because we'll always have a value for the course)
        self.labels = ['cwid', 'name', 'major', 'courses']

    def add_course(self, course, grade):
        """A function that assigns a value grade to the key course."""
        self.courses[course] = grade
    
    def pt_row(self):
        """"A function that creates rows with student's information."""
        return [self.cwid, self.name, sorted(self.courses.keys())]
    

class Instructor:
    """A class that stores all the information about instructors."""
    pt_hdr = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.students = defaultdict(int) #defaultdict specifies only value type

    def add_course(self, course):
        self.students[course] += 1
    
    def pt_row(self):
        """A function that creates rows with instructor's information."""
        for course, num_students in self.students.items():
            yield [self.cwid, self.name, self.department, course, num_students]


class Repository:
    """A class that stores information about students and instructors and generates tables of students and instructors."""
    def __init__(self, path, ptables =True):
        self.students = dict() #cwid is the key, Instance of class Student is the value
        self.instructors = dict() #cwid is they, Instance of class Instructor is the value
        self.grades = list()

        self.reading_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))

        if ptables:
            print("\nStudent Summary")
            self.student_table()

            print("\nInstructor Summary")
            self.instructor_table()

    def student_table(self):
        """A function that creates a table with student's information."""
        pt = PrettyTable(field_names = Student.pt_hdr)
        for student in self.students.values():
            pt.add_row(student.pt_row())
        print (pt)
    
    def instructor_table(self):
        """A function that creates a table with instructor's information."""
        pt = PrettyTable(field_names = Instructor.pt_hdr)
        for instructor in self.instructors.values():
            for row in instructor.pt_row():
                pt.add_row(row) 
        print (pt)

    def reading_students(self, path):
        """A function that assigns student's information (cwid, name, major) to his/her cwid."""
        try:
            for cwid, name, major in read_file(path, 3, '\t', header=False):
                self.students[cwid] = Student(cwid, name, major)
        except ValueError as e:
            print(e)
    
    def get_instructors(self, path):
        """A function that assigns instructor's information (cwid, name, dept) to instructor's cwid."""
        try:
            for cwid, name, dept in read_file(path, 3, sep = '\t', header=False):
                self.instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as e:
            print(e)
    
    def get_grades(self, path):
        """A function that adds courses and grades to students and instructors."""
        try:
            for student_cwid, course, grade, instructor_cwid in read_file(path, 4, sep = '\t', header=False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_course(course, grade)
                else:
                    print("unknown student")
                if instructor_cwid in self.instructors:
                    self.instructors[instructor_cwid].add_course(course)
                else:
                    print("instructor not found")
        except ValueError as e:
            print (e)

def main():
    path = (r'C:\Users\Kat\Documents\VSC-Python\810\Repository')
    stevens = Repository(path)
   

if __name__ == '__main__':
    main()