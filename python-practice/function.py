#                                   *** --- Student Learning Management System --- ***

students = []  # List to store student data

def add_students():
    # Input for new student details
    new_student = input("NAME OF STUDENT = ")
    class_sec = input("ENTER YOUR CLASS = ")
    dob = input("ENTER YOUR DOB = ")
    group_selection = ("""
Group Selection:
                       
1. Computer Science
2. Biology
3. General
4. Arts
5. Commerce
                       """)
    print(group_selection)
    group = input("WHICH IS YOUR GROUP = ") 

    # Lowercase inputs to standardize, although you may not need this for final output
    new_student = new_student.lower()
    class_sec = class_sec.lower()
    dob = dob.lower()
    group = group.lower()

    # Storing student details as a dictionary in the students list
    student_details = {
        "name": new_student,
        "class": class_sec,
        "dob": dob,
        "group": group
    }
    students.append(student_details)

    # Display student details in a formatted way
    details = (f"""
Details:

Student Name  : {new_student.upper()}
Class/Section : {class_sec.upper()}
Group         : {group.upper()}
DATE OF BIRTH : {dob.upper()} 
                 """)
    print(details)


def remove_students():
    # Get student name to remove
    student_name = input("Enter the name of the student to remove: ").lower()

    # Find and remove student by name
    global students
    students = [student for student in students if student["name"] != student_name]

    print(f"Student '{student_name.upper()}' removed successfully.")


def see_students():
    if not students:
        print("No students to display.")
        return

    print("Student List:")
    for student in students:
        details = (f"""
Details:

Student Name  : {student['name'].upper()}
Class/Section : {student['class'].upper()}
Group         : {student['group'].upper()}
DATE OF BIRTH : {student['dob'].upper()} 
                 """)
        print(details)


def exit_system():
    print("Exiting the system...")
    exit()


def main():
    while True:
        print("\nWelcome to the Student Learning Management System")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. See Students")
        print("4. Exit")
        
        choice = input("Please select an option: ")
        
        if choice == "1":
            add_students()
        elif choice == "2":
            remove_students()
        elif choice == "3":
            see_students()
        elif choice == "4":
            exit_system()
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
