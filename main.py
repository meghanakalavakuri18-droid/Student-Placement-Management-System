
import sqlite3

db = sqlite3.connect("placement.db")
db.execute("""CREATE TABLE IF NOT EXISTS students(
roll TEXT PRIMARY KEY, name TEXT, branch TEXT,
email TEXT, cgpa REAL)""")
db.execute("""CREATE TABLE IF NOT EXISTS companies(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT, role TEXT, min_cgpa REAL, package REAL)""")
db.execute("""CREATE TABLE IF NOT EXISTS applications(
roll TEXT, company_id INTEGER, status TEXT DEFAULT 'Applied',
UNIQUE(roll, company_id))""")
db.commit()


def add_student():
    data = (
        input("Roll number: "),
        input("Name: "),
        input("Branch: "),
        input("Email: "),
        float(input("CGPA (0-10): "))
    )
    try:
        db.execute("INSERT INTO students VALUES(?,?,?,?,?)", data)
        db.commit()
        print("Student added!")
    except sqlite3.IntegrityError:
        print("Roll number already exists.")


def view_students():
    for s in db.execute("SELECT * FROM students"):
        print(s)


def add_company():
    name = input("Company name: ")
    role = input("Job role: ")
    cgpa = float(input("Minimum CGPA: "))
    package = float(input("Package (LPA): "))
    db.execute(
        "INSERT INTO companies(name,role,min_cgpa,package) VALUES(?,?,?,?)",
        (name, role, cgpa, package)
    )
    db.commit()
    print("Company added!")


def view_companies():
    for c in db.execute("SELECT * FROM companies"):
        print(c)


def apply():
    roll = input("Student roll number: ")
    try:
        cid = int(input("Company ID: "))
    except ValueError:
        print("Invalid company ID.")
        return

    student = db.execute(
        "SELECT cgpa FROM students WHERE roll=?", (roll,)
    ).fetchone()
    company = db.execute(
        "SELECT min_cgpa FROM companies WHERE id=?", (cid,)
    ).fetchone()

    if not student or not company:
        print("Student or company not found.")
    elif student[0] < company[0]:
        print("Student is not eligible.")
    else:
        try:
            db.execute(
                "INSERT INTO applications(roll,company_id) VALUES(?,?)",
                (roll, cid)
            )
            db.commit()
            print("Application submitted!")
        except sqlite3.IntegrityError:
            print("Already applied.")


def view_applications():
    query = """
    SELECT a.roll, s.name, c.name, c.role, a.status
    FROM applications a
    JOIN students s ON a.roll=s.roll
    JOIN companies c ON a.company_id=c.id
    """
    for row in db.execute(query):
        print(row)


def main():
    print("Student Placement Management System")

    while True:
        print("""
1. Add Student
2. View Students
3. Add Company
4. View Companies
5. Apply for Placement
6. View Applications
0. Exit
""")
        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            add_company()
        elif choice == "4":
            view_companies()
        elif choice == "5":
            apply()
        elif choice == "6":
            view_applications()
        elif choice == "0":
            db.close()
            print("Program closed.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
