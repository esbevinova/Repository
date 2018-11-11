"""SSW-810-A
   Ekaterina (katya) Bevinova
   HW10
"""
from prettytable import PrettyTable
from HW08ebevinova import read_file
import unittest
import os
from collections import defaultdict
import sqlite3

class Student:
    "A class that stores all the information about students."
    pt_hdr = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict() #key is course, value is grade (we're not using defaultdict because we'll always have a value for the course)
        self.labels = ['cwid', 'name', 'major', 'courses']

    def add_course(self, course, grade):
        """A function that assigns a value grade to the key course."""
        self.courses[course] = grade
    
    def pt_row(self, maj):
        """"A function that creates rows with student's information."""
        completed_courses, remaining_required, remaining_electives = maj.calculated_courses(self.courses)
        return [self.cwid, self.name, self.major, completed_courses, remaining_required, remaining_electives]
    

class Majors:
    "A class that stores all the information about required and elective courses."
    pt_hdr = ['Dept', 'Required', 'Electives']
    def __init__(self, dept):
        self.dept = dept
        self.required = set()
        self.electives = set()
        
    
    def add(self, flag, course):
        if flag == 'R':
            self.required.add(course)
        elif flag == 'E':
            self.electives.add(course)     
    
    def calculated_courses(self, courses):
        """Return completed_courses, remaining_required, remaining_electives where courses is dict with key as a course and value as a grade"""
        remaining_required = self.required
        remaining_electives = self.electives
        completed_courses = set()

        for course, grade in courses.items():
            if grade in ('A', 'A-', 'B+', 'B-', 'B', 'C', 'C-', 'C+'):
                completed_courses.add(course)
            
        remaining_required = self.required - completed_courses
            
        if self.electives.intersection(completed_courses):
            remaining_electives = None
            
        return completed_courses, remaining_required, remaining_electives
    
    def pt_row(self):
        return [self.dept, self.required, self.electives]
    

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
        self.majors = dict() #major is the key, Instance of class Majors is the value

        self.reading_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))
        self.reading_majors(os.path.join(path, 'majors.txt'))

        

        if ptables:
            print("\nStudent Summary")
            self.student_table()

            print("\nInstructor Summary")
            self.instructor_table()

            print("\nMajors Summary")
            self.majors_table()

    def majors_table(self):
        pt = PrettyTable(field_names = Majors.pt_hdr)
        for dept in self.majors.values():
            pt.add_row(dept.pt_row())
        print (pt)

    def student_table(self):
        """A function that creates a table with student's information."""
        pt = PrettyTable(field_names = Student.pt_hdr)
        for student in self.students.values():
            pt.add_row(student.pt_row(self.majors[student.major]))
        print (pt)
    
    def instructor_table(self):
        """A function that creates a table with instructor's information that is extracted from External Database."""
        DB_FILE = "C:\sql\810_startup.db"
        db = sqlite3.connect(DB_FILE)
        pt = PrettyTable(field_names = Instructor.pt_hdr)
        query = "select CWID, Name, Dept, Course, count(Course) as Students from (select * from HW11_instructors left join HW11_grades on  Instructor_CWID = CWID) group by Course order by CWID DESC "
        for row in db.execute(query):
                pt.add_row(row) 
        print (pt)

    def reading_majors(self, path):
        try:
            for dept, flag, course in read_file(path, 3, '\t', header=False):
                if dept not in self.majors: #if dept is not in majors (dict) then we add a new instance of it
                    self.majors[dept] = Majors(dept)
                self.majors[dept].add(flag, course) #add flag, course to the major through every line
        except ValueError as e:
            print (e)

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