"""SSW-810-A
   Ekaterina (katya) Bevinova
   HW12
"""
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)
   
@app.route('/instructors_table')
def instructors_table():
    DB_FILE = r"C:\sql\810_startup.db"
    query = "select CWID, Name, Dept, Course, count(Course) as Students from (select * from HW11_instructors left join HW11_grades on  Instructor_CWID = CWID) group by Course order by CWID DESC " 
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    data = [{'Cwid': cwid, 'Name': name, 'Dept': dept, 'Course': course, 'Students': students}
                for cwid, name, dept, course, students in results]
    
    db.close()
    return render_template('instructors_table.html',
                            title='Stevens Repository',
                            table_title="Number of students by course and instructor",
                            instructors=data)
app.run(debug=True)
