## **---Empty List For Managing History---** ##

students = []

## **--- Adding Students Function---** ##

def add_students(students):
    print("-----------------------------------------------------------------------------------")
    print("Adding Student")
    print("-----------------------------------------------------------------------------------")
    name = input("Name of the student: ")
    grade = input("Class of the student: ")
    age = input("Age of the student: ") 

    students.append(name)
    students.append(grade)
    students.append(age)
    return students

## **--- Removing Students Function---** ##

def remove_students(students):
    print("-----------------------------------------------------------------------------------")
    print("Removing Student")
    print("-----------------------------------------------------------------------------------")
    name = input("Name of student: ")
    grade = input("Class of stuednt: ")
    age = input("Age of student: ")

    if name and grade and age in students:
        students.remove(name)
        students.remove(grade)
        students.remove(age)
        return students

## **--- View Students Function---** ##

def view_all(students):
    print("-----------------------------------------------------------------------------------")
    print("See all students")
    print("-----------------------------------------------------------------------------------")
    print(f"All Students: {students}")

print("-----------------------------------------------------------------------------------")
print("Welcome to Student Managment System Programe.")

## **--- Program Excuting Code---** ##

while True:

    ## **--- Printing All Options---** ##

    options = ("""
Choose Any One:

1. Add Student
2. Remove Student
3. Veiw All
4. Exit
    """)
    print("-----------------------------------------------------------------------------------")
    print(options)
    print("-----------------------------------------------------------------------------------")

    user = input("Choose Any One: ")
    
## **--- Conditoins For Different Functions---** ##

    if user == "1":
        add_students(students)

    elif user == "2":
        remove_students(students)

    elif user == "3":
        view_all(students)

    else:
        print("-----------------------------------------------------------------------------------")
        print("Thanks!")
        print("-----------------------------------------------------------------------------------")

    if user == "4":
        break




        

