import csv
import tkinter as tk
from tkinter import messagebox

class UserType:
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"
    MANAGER = "MANAGER"

class User:
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.type = user_type

class SignUpManager:
    def __init__(self):
        self.users = []

    def register_user(self, username, password, user_type):
        for user in self.users:
            if user.username == username:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                return False

        self.users.append(User(username, password, user_type))
        messagebox.showinfo("Success", "User registered successfully!")
        return True

    def get_users(self):
        return self.users

class LoginManager:
    def __init__(self, user_list):
        self.current_user = None
        self.users = user_list

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = User(username, password, user.type)
                messagebox.showinfo("Success", "Login successful!")
                return True

        messagebox.showerror("Error", "Login failed. Invalid username or password.")
        return False

    def get_current_user_type(self):
        return self.current_user.type if self.is_logged_in() else UserType.STUDENT

    def is_logged_in(self):
        return self.current_user is not None

    def get_current_username(self):
        return self.current_user.username if self.is_logged_in() else "No user logged in"

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Success", "Logout successful!")

class Student:
    def __init__(self, name, father_name, mother_name, address, blood_group, roll_number, grade):
        self.name = name
        self.father_name = father_name
        self.mother_name = mother_name
        self.address = address
        self.blood_group = blood_group
        self.roll_number = roll_number
        self.grade = grade

    def save_to_file(self, file):
        file.write(f"{self.name},{self.father_name},{self.mother_name},{self.address},"
                   f"{self.blood_group},{self.roll_number},{self.grade}\n")

    def modify_details(self):
        self.name = input("Enter updated student name: ")
        self.father_name = input("Enter updated father's name: ")
        self.mother_name = input("Enter updated mother's name: ")
        self.address = input("Enter updated address: ")
        self.blood_group = input("Enter updated blood group: ")
        self.roll_number = int(input("Enter updated roll number: "))
        self.grade = float(input("Enter updated grade: "))

    def matches_search_criteria(self, search_term):
        lower_name = self.name.lower()
        lower_search_term = search_term.lower()
        return (lower_name.find(lower_search_term) != -1) or (str(self.roll_number).find(search_term) != -1)

class Instructor:
    class Lecture:
        def __init__(self, course_name, lecture_file_name):
            self.course_name = course_name
            self.lecture_file_name = lecture_file_name

    def __init__(self, name, cnic, doj):
        self.name = name
        self.cnic = cnic
        self.doj = doj
        self.uploaded_lectures = []
        self.enrolled_quizzes = []
        self.enrolled_courses = []

    def upload_lecture(self, course_name, lecture_file_name):
        self.uploaded_lectures.append(self.Lecture(course_name, lecture_file_name))
        with open("lectures_data.csv", "a") as lecture_file:
            lecture_file.write(f"{course_name},{lecture_file_name}\n")

        print(f"Lecture uploaded successfully for course: {course_name}")

    def view_uploaded_lectures(self):
        if not self.uploaded_lectures:
            print("No lectures uploaded.")
        else:
            print("Uploaded Lectures:")
            for lecture in self.uploaded_lectures:
                print(f"Course: {lecture.course_name}, File: {lecture.lecture_file_name}")

    def save_to_file(self, file):
        file.write(f"{self.name},{self.cnic},{self.doj}\n")

    def modify_details(self):
        self.name = input("Enter updated Instructor name: ")
        self.cnic = int(input("Enter updated CNIC: "))
        self.doj = input("Enter updated date of joining: ")

    def matches_search_criteria(self, search_term):
        lower_name = self.name.lower()
        lower_search_term = search_term.lower()
        return (lower_name.find(lower_search_term) != -1) or (str(self.cnic).find(search_term) != -1)

    def view_enrolled_quizzes(self):
        if not self.enrolled_quizzes:
            print("No quizzes enrolled.")
        else:
            print("Enrolled Quizzes:")
            for quiz in self.enrolled_quizzes:
                print(quiz)

    def add_lecture(self, course_name):
        print(f"Added a lecture to course: {course_name}")

    def add_quiz(self, course_name):
        print(f"Added a quiz to course: {course_name}")

    def view_enrolled_courses(self):
        if not self.enrolled_courses:
            print("No courses enrolled.")
        else:
            print("Enrolled Courses:")
            for course in self.enrolled_courses:
                print(course)

    def enroll_in_quiz(self, quiz_name):
        self.enrolled_quizzes.append(quiz_name)
        print(f"Enrolled in quiz: {quiz_name}")

    def enroll_in_course(self, course_name):
        self.enrolled_courses.append(course_name)
        print(f"Enrolled in course: {course_name}")

class StudentManager:
    def __init__(self):
        self.students = []
        self.instructors = []

    def add_student(self, student):
        self.students.append(student)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)

    def set_students(self, new_students):
        self.students = new_students

    def set_instructors(self, new_instructors):
        self.instructors = new_instructors

    def save_student_records(self):
        with open("student_records.csv", "a") as file:
            self.students[-1].save_to_file(file)

        messagebox.showinfo("Success", "Student record added and saved successfully.")

    def save_instructor_records(self):
        with open("instructor_records.csv", "a") as file:
            self.instructors[-1].save_to_file(file)

        messagebox.showinfo("Success", "Instructor record added and saved successfully.")

    def get_student_count(self):
        return len(self.students)

    def get_instructor_count(self):
        return len(self.instructors)

    def get_students(self):
        return self.students

    def get_instructors(self):
        return self.instructors

    def modify_student_details(self):
        students = read_data_from_csv("student_records.csv")
        search_term = input("Enter student name or roll number to modify: ")

        index = -1
        for i, student in enumerate(students):
            if student.matches_search_criteria(search_term):
                if index != -1:
                    print("Error: Multiple students match the search criteria. "
                          "Please provide a more specific search term.")
                    return
                index = i

        if index == -1:
            print("No matching student found.")
            return

        students[index].modify_details()
        write_data_to_csv("student_records.csv", students)
        print("Student details modified successfully.")

def read_data_from_csv(file_name):
    data = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def write_data_to_csv(file_name, data):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Tkinter GUI
import csv
import tkinter as tk
from tkinter import messagebox, simpledialog

# [Existing Class Definitions: UserType, User, SignUpManager, LoginManager, Student, Instructor, StudentManager]

class SignupWindow(tk.Toplevel):
    def __init__(self, parent, sign_up_manager):
        super().__init__(parent)
        self.sign_up_manager = sign_up_manager
        self.title("Signup")

        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(self, text="User Type:").grid(row=2, column=0)
        self.user_type_entry = tk.Entry(self)
        self.user_type_entry.grid(row=2, column=1)

        tk.Button(self, text="Signup", command=self.signup).grid(row=3, column=0, columnspan=2)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_entry.get()

        if user_type not in [UserType.STUDENT, UserType.INSTRUCTOR, UserType.MANAGER]:
            messagebox.showerror("Error", "Invalid user type. Choose from STUDENT, INSTRUCTOR, MANAGER.")
            return

        if self.sign_up_manager.register_user(username, password, user_type):
            messagebox.showinfo("Success", "User registered successfully!")
            self.destroy()
    

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Student Management System")

        self.sign_up_manager = SignUpManager()
        self.login_manager = LoginManager(self.sign_up_manager.get_users())
        self.student_manager = StudentManager()

        self.create_widgets()

    def create_widgets(self):
        # Login Frame
        login_frame = tk.Frame(self)
        login_frame.pack(padx=10, pady=10)

        tk.Label(login_frame, text="Username:").grid(row=0, column=0)
        tk.Label(login_frame, text="Password:").grid(row=1, column=0)

        self.username_entry = tk.Entry(login_frame)
        self.password_entry = tk.Entry(login_frame, show="*")

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)

        tk.Button(login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(login_frame, text="Signup", command=self.open_signup).grid(row=3, column=0, columnspan=2, pady=10)

        # Student Management Frame
        student_management_frame = tk.Frame(self)
        student_management_frame.pack(padx=10, pady=10)

        tk.Button(student_management_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, pady=5)
        tk.Button(student_management_frame, text="Modify Student", command=self.modify_student).grid(row=1, column=0, pady=5)
        tk.Button(student_management_frame, text="Save Student Records", command=self.save_student_records).grid(row=2, column=0, pady=5)

        # Instructor Management Frame
        instructor_management_frame = tk.Frame(self)
        instructor_management_frame.pack(padx=10, pady=10)

        tk.Button(instructor_management_frame, text="Add Instructor", command=self.add_instructor).grid(row=0, column=0, pady=5)
        tk.Button(instructor_management_frame, text="Modify Instructor", command=self.modify_instructor).grid(row=1, column=0, pady=5)
        tk.Button(instructor_management_frame, text="Save Instructor Records", command=self.save_instructor_records).grid(row=2, column=0, pady=5)

        # Status Label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.login_manager.login(username, password):
            self.status_label["text"] = f"Logged in as {self.login_manager.get_current_username()}, UserType: {self.login_manager.get_current_user_type()}"
        else:
            self.status_label["text"] = "Login failed. Invalid username or password."

    def open_signup(self):
        SignupWindow(self, self.sign_up_manager)
    def add_student(self):
        new_student_window = tk.Toplevel(self)
        new_student_window.title("Add Student")

    # Define and place widgets for student details
        tk.Label(new_student_window, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(new_student_window)
        name_entry.grid(row=0, column=1)

        tk.Label(new_student_window, text="Father's Name:").grid(row=1, column=0)
        father_name_entry = tk.Entry(new_student_window)
        father_name_entry.grid(row=1, column=1)

        tk.Label(new_student_window, text="Mother's Name:").grid(row=2, column=0)
        mother_name_entry = tk.Entry(new_student_window)
        mother_name_entry.grid(row=2, column=1)

        tk.Label(new_student_window, text="Address:").grid(row=3, column=0)
        address_entry = tk.Entry(new_student_window)
        address_entry.grid(row=3, column=1)

        tk.Label(new_student_window, text="Blood Group:").grid(row=4, column=0)
        blood_group_entry = tk.Entry(new_student_window)
        blood_group_entry.grid(row=4, column=1)

        tk.Label(new_student_window, text="Roll Number:").grid(row=5, column=0)
        roll_number_entry = tk.Entry(new_student_window)
        roll_number_entry.grid(row=5, column=1)

        tk.Label(new_student_window, text="Grade:").grid(row=6, column=0)
        grade_entry = tk.Entry(new_student_window)
        grade_entry.grid(row=6, column=1)

    # Function to submit student dat
        def submit_student():
        # Collect data from the entries
            name = name_entry.get()
            father_name = father_name_entry.get()
            mother_name = mother_name_entry.get()
            address = address_entry.get()
            blood_group = blood_group_entry.get()
            roll_number = roll_number_entry.get()
            grade = grade_entry.get()

        # Validation or transformation of data can be done here

        # Create a new Student object
            new_student = Student(name, father_name, mother_name, address, blood_group, roll_number, grade)
            self.student_manager.add_student(new_student)
            messagebox.showinfo("Success", "Student added successfully!")
            new_student_window.destroy()

        tk.Button(new_student_window, text="Submit", command=submit_student).grid(row=7, column=0, columnspan=2)

    def modify_student(self):
        modify_student_window = tk.Toplevel(self)
        modify_student_window.title("Modify Student")
# Define widgets to search for a student (e.g., by name or roll number)
        tk.Label(modify_student_window, text="Enter Student Name or Roll Number:").grid(row=0, column=0)
        search_entry = tk.Entry(modify_student_window)
        search_entry.grid(row=0, column=1)

    # Function to find and modify student
        def find_and_modify_student():
         search_term = search_entry.get()
         found_students = [student for student in self.student_manager.get_students() if student.matches_search_criteria(search_term)]

         if len(found_students) == 0:
            messagebox.showerror("Error", "No matching student found.")
            return
         elif len(found_students) > 1:
            messagebox.showerror("Error", "Multiple students match the search criteria. Please provide a more specific term.")
            return

        # Assuming the first match is the one we want
         student_to_modify = found_students[0]

        # Open a new window to modify student details
         modify_details_window = tk.Toplevel(modify_student_window)
         modify_details_window.title("Modify Student Details")

        # Widgets for modifying details
         tk.Label(modify_details_window, text="Name:").grid(row=0, column=0)
         name_entry = tk.Entry(modify_details_window)
         name_entry.insert(0, student_to_modify.name)
         name_entry.grid(row=0, column=1)

        # Similar widgets for other student details...
        # For example, father's name, mother's name, address, etc.

         def submit_modified_details():
            # Updating the student's details
            student_to_modify.name = name_entry.get()
            # Update other fields similarly...

            messagebox.showinfo("Success", "Student details modified successfully.")

         tk.Button(modify_details_window, text="Submit Changes", command=submit_modified_details).grid(row=8, column=0, columnspan=2)

        tk.Button(modify_student_window, text="Find and Modify", command=find_and_modify_student).grid(row=1, column=0, columnspan=2)
    def add_instructor(self):
        new_instructor_window = tk.Toplevel(self)
        new_instructor_window.title("Add Instructor")

    # Define and place widgets here for instructor details like name, CNIC, etc.
        tk.Label(new_instructor_window, text="Name:").grid(row=0, column=0)
        name_entry = tk.Entry(new_instructor_window)
        name_entry.grid(row=0, column=1)

        tk.Label(new_instructor_window, text="CNIC:").grid(row=1, column=0)
        cnic_entry = tk.Entry(new_instructor_window)
        cnic_entry.grid(row=1, column=1)

        tk.Label(new_instructor_window, text="Date of Joining (YYYY-MM-DD):").grid(row=2, column=0)
        doj_entry = tk.Entry(new_instructor_window)
        doj_entry.grid(row=2, column=1)

    # Additional fields can be added similarly...
        def submit_instructor():
        # Collect data from the entries
            name = name_entry.get()
            cnic = cnic_entry.get()
            doj = doj_entry.get()

        # Validation or transformation of data can be done here

        # Create a new Instructor object
            new_instructor = Instructor(name, cnic, doj)
            self.student_manager.add_instructor(new_instructor)
            messagebox.showinfo("Success", "Instructor added successfully!")
            new_instructor_window.destroy()

            tk.Button(new_instructor_window, text="Submit", command=submit_instructor).grid(row=8, column=0, columnspan=2)
    def modify_instructor(self):
        modify_instructor_window = tk.Toplevel(self)
        modify_instructor_window.title("Modify Instructor")

    # Define widgets to search for an instructor (e.g., by name or CNIC)
        tk.Label(modify_instructor_window, text="Enter Instructor Name or CNIC:").grid(row=0, column=0)
        search_entry = tk.Entry(modify_instructor_window)
        search_entry.grid(row=0, column=1)

    # Function to find and modify instructor
        def find_and_modify_instructor():
            search_term = search_entry.get()
            found_instructors = [instructor for instructor in self.student_manager.get_instructors() if instructor.matches_search_criteria(search_term)]

            if len(found_instructors) == 0:
                messagebox.showerror("Error", "No matching instructor found.")
                return
            elif len(found_instructors) > 1:
                messagebox.showerror("Error", "Multiple instructors match the search criteria. Please provide a more specific term.")
                return

        # Assuming the first match is the one we want
            instructor_to_modify = found_instructors[0]

        # Open a new window to modify instructor details
            modify_details_window = tk.Toplevel(modify_instructor_window)
            modify_details_window.title("Modify Instructor Details")

        # Widgets for modifying details
            tk.Label(modify_details_window, text="Name:").grid(row=0, column=0)
            name_entry = tk.Entry(modify_details_window)
            name_entry.insert(0, instructor_to_modify.name)
            name_entry.grid(row=0, column=1)

            tk.Label(modify_details_window, text="CNIC:").grid(row=1, column=0)
            cnic_entry = tk.Entry(modify_details_window)
            cnic_entry.insert(0, instructor_to_modify.cnic)
            cnic_entry.grid(row=1, column=1)

            tk.Label(modify_details_window, text="Date of Joining (YYYY-MM-DD):").grid(row=2, column=0)
            doj_entry = tk.Entry(modify_details_window)
            doj_entry.insert(0, instructor_to_modify.doj)
            doj_entry.grid(row=2, column=1)

        # Additional fields can be added similarly...

            def submit_modified_details():
            # Updating the instructor's details
                instructor_to_modify.name = name_entry.get()
                instructor_to_modify.doj = doj_entry.get()
            # Update other fields similarly...

                messagebox.showinfo("Success", "Instructor details modified successfully.")
                modify_details_window.destroy()

            tk.Button(modify_details_window, text="Submit Changes", command=submit_modified_details).grid(row=8, column=0, columnspan=2)

        tk.Button(modify_instructor_window, text="Find and Modify", command=find_and_modify_instructor).grid(row=1, column=0, columnspan=2)

    def save_student_records(self):
        with open("student_records.csv", "w", newline='') as file:
            writer = csv.writer(file)
        # Assuming that each student object has attributes: name, father_name, mother_name, address, blood_group, roll_number, grade
            for student in self.student_manager.get_students():
                writer.writerow([student.name, student.father_name, student.mother_name, student.address, student.blood_group, student.roll_number, student.grade])
        messagebox.showinfo("Success", "Student records saved successfully.")
    def save_instructor_records(self):
        with open("instructor_records.csv", "w", newline='') as file:
            writer = csv.writer(file)
        # Assuming that each instructor object has attributes: name, cnic, doj
            for instructor in self.student_manager.get_instructors():
                writer.writerow([instructor.name, instructor.cnic, instructor.doj])
        messagebox.showinfo("Success", "Instructor records saved successfully.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
