import tkinter as tk
from enum import Enum

class UserType(Enum):
    STUDENT = 1
    INSTRUCTOR = 2
    MANAGER = 3

class User:
    def __init__(self, uname, pwd, utype):
        self.username = uname
        self.password = pwd
        self.type = utype

class SignUpManager:
    def __init__(self):
        self.users = []

    def register_user(self, username, password, user_type):
        for user in self.users:
            if user.username == username:
                print("Error: Username already exists. Please choose a different username.")
                return False

        self.users.append(User(username, password, user_type))
        print("User registered successfully!")
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
                self.current_user = User(user.username, user.password, user.type)
                print("Login successful!")
                return True

        print("Login failed. Invalid username or password.")
        return False

    def get_current_user_type(self):
        return self.current_user.type if self.is_logged_in() else UserType.STUDENT

    def is_logged_in(self):
        return self.current_user is not None

    def get_current_username(self):
        return self.current_user.username if self.is_logged_in() else "No user logged in"

    def logout(self):
        self.current_user = None
        print("Logout successful!")

# Tkinter GUI Implementation
class UserRegistrationApp:
    def __init__(self, signup_manager):
        self.signup_manager = signup_manager
        self.root = tk.Tk()
        self.root.title("User Registration")

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_entry = tk.Entry(self.root)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_entry = tk.Entry(self.root, show="*")

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.register_button.pack()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.signup_manager.register_user(username, password, UserType.STUDENT):
            print(f"Registered User: {username}")

import csv
import os

from tkinter import messagebox

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
        file.write(f"{self.name},{self.father_name},{self.mother_name},{self.address},{self.blood_group},{self.roll_number},{self.grade}\n")

    def modify_details(self):
        print("Enter updated student name:", end=" ")
        self.name = input()
        print("Enter updated father's name:", end=" ")
        self.father_name = input()
        print("Enter updated mother's name:", end=" ")
        self.mother_name = input()
        print("Enter updated address:", end=" ")
        self.address = input()
        print("Enter updated blood group:", end=" ")
        self.blood_group = input()
        print("Enter updated roll number:", end=" ")
        self.roll_number = int(input())
        print("Enter updated grade:", end=" ")
        self.grade = float(input())

    def matches_search_criteria(self, search_term):
        lower_name = self.name.lower()
        lower_search_term = search_term.lower()
        return (lower_name.find(lower_search_term) != -1) or (str(self.roll_number).find(search_term) != -1)


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def save_student_records(self):
        with open("student_records.csv", "a") as file:
            self.students[-1].save_to_file(file)
        print("Student record added and saved successfully.")

    def display_all_students(self):
        for i, student in enumerate(self.students):
            print(f"Student {i + 1}:")
            print(f"Name: {student.name}")
            print(f"Father's Name: {student.father_name}")
            print(f"Mother's Name: {student.mother_name}")
            print(f"Address: {student.address}")
            print(f"Blood Group: {student.blood_group}")
            print(f"Roll Number: {student.roll_number}")
            print(f"Grade: {student.grade}")
            print("\n")

    def search_students(self, search_term):
        matching_indices = [i for i, student in enumerate(self.students) if student.matches_search_criteria(search_term)]

        if not matching_indices:
            print("No students found matching the search criteria.")
        else:
            print("Students matching the search criteria:")
            for index in matching_indices:
                student = self.students[index]
                print(f"Student {index + 1}:")
                print(f"Name: {student.name}")
                print(f"Father's Name: {student.father_name}")
                print(f"Mother's Name: {student.mother_name}")
                print(f"Address: {student.address}")
                print(f"Blood Group: {student.blood_group}")
                print(f"Roll Number: {student.roll_number}")
                print(f"Grade: {student.grade}")
                print("\n")

    def read_data_from_csv(self, file_path):
        data = []
        if os.path.exists(file_path):
            with open(file_path, newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(Student(*row))
        return data

    def write_data_to_csv(self, data, file_path):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            for student in data:
                writer.writerow([student.name, student.father_name, student.mother_name,
                                 student.address, student.blood_group, student.roll_number, student.grade])

class StudentRegistrationApp:
    def __init__(self, student_manager):
        self.student_manager = student_manager
        self.root = tk.Tk()
        self.root.title("Student Registration")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_entry = tk.Entry(self.root)

        self.father_name_label = tk.Label(self.root, text="Father's Name:")
        self.father_name_entry = tk.Entry(self.root)

        self.mother_name_label = tk.Label(self.root, text="Mother's Name:")
        self.mother_name_entry = tk.Entry(self.root)

        self.address_label = tk.Label(self.root, text="Address:")
        self.address_entry = tk.Entry(self.root)

        self.blood_group_label = tk.Label(self.root, text="Blood Group:")
        self.blood_group_entry = tk.Entry(self.root)

        self.roll_number_label = tk.Label(self.root, text="Roll Number:")
        self.roll_number_entry = tk.Entry(self.root)

        self.grade_label = tk.Label(self.root, text="Grade:")
        self.grade_entry = tk.Entry(self.root)

        self.register_button = tk.Button(self.root, text="Register", command=self.register_student)

        self.name_label.pack()
        self.name_entry.pack()
        self.father_name_label.pack()
        self.father_name_entry.pack()
        self.mother_name_label.pack()
        self.mother_name_entry.pack()
        self.address_label.pack()
        self.address_entry.pack()
        self.blood_group_label.pack()
        self.blood_group_entry.pack()
        self.roll_number_label.pack()
        self.roll_number_entry.pack()
        self.grade_label.pack()
        self.grade_entry.pack()
        self.register_button.pack()

    def register_student(self):
        name = self.name_entry.get()
        father_name = self.father_name_entry.get()
        mother_name = self.mother_name_entry.get()
        address = self.address_entry.get()
        blood_group = self.blood_group_entry.get()
        roll_number = int(self.roll_number_entry.get())
        grade = float(self.grade_entry.get())

        student = Student(name, father_name, mother_name, address, blood_group, roll_number, grade)
        self.student_manager.add_student(student)
        self.student_manager.save_student_records()

        messagebox.showinfo("Registration", f"Student {name} registered successfully!")


class Course:
    def __init__(self, name, course_id, capacity):
        self.course_name = name
        self.course_id = course_id
        self.capacity = capacity
        self.enrolled_students = []
        self.uploaded_lectures = []

    def enroll_student(self, student_id):
        if len(self.enrolled_students) < self.capacity:
            self.enrolled_students.append(student_id)
            return True
        return False

    def upload_lecture(self, lecture_name):
        self.uploaded_lectures.append(lecture_name)

    def get_uploaded_lectures(self):
        return self.uploaded_lectures

    def __str__(self):
        return f"{self.course_name},{self.course_id},{self.capacity}"


class CourseManager:
    def __init__(self, student_manager):
        self.courses = []
        self.student_manager = student_manager

    def get_courses(self):
        return self.courses

    def add_course(self, course):
        self.courses.append(course)

    def set_courses(self, new_courses):
        self.courses = new_courses

    def display_all_courses(self):
        for i, course in enumerate(self.courses):
            print(f"Course {i + 1}:")
            print(f"Name: {course.course_name}")
            print(f"ID: {course.course_id}")
            print(f"Capacity: {course.capacity}")
            print(f"Enrolled Students: {len(course.enrolled_students)}")
            print()

    def save_courses(self):
        self.write_data_to_csv(self.courses, "courses_data.csv")

    def modify_course(self, course_id, updated_course):
        if 1 <= course_id <= len(self.courses):
            self.courses[course_id - 1] = updated_course
            return True
        return False

    def enroll_student_in_course(self, student_id, course_name):
        for course in self.courses:
            if course.course_name == course_name:
                student_already_enrolled = student_id in course.enrolled_students
                if not student_already_enrolled:
                    course.enrolled_students.append(student_id)

                    with open("enrolled_students.csv", "a") as enrolled_file:
                        enrolled_file.write(f"{course_name},{student_id}\n")

                    with open("courses_data.csv", "w") as courses_file:
                        for c in self.courses:
                            courses_file.write(f"{c.course_name},{c.capacity},{len(c.enrolled_students)}\n")

                    print("Student enrolled successfully in the course!")
                    return True
                else:
                    print("Error: Student is already enrolled in the course.")
                break

        print("Error: Course not found.")
        return False

    def enroll_student_in_course_manager(self, student_id, course_name):
        self.student_manager.enroll_student_in_course(self, student_id, course_name)

    def write_data_to_csv(self, data, file_path):
        with open(file_path, "w", newline="") as file:
            for item in data:
                file.write(f"{item}\n")


import tkinter as tk
from tkinter import messagebox
from enum import Enum

class UserType(Enum):
    STUDENT = 1
    INSTRUCTOR = 2
    MANAGER = 3

class User:
    def __init__(self, uname, pwd, utype):
        self.username = uname
        self.password = pwd
        self.type = utype

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
                self.current_user = User(user.username, user.password, user.type)
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

# Tkinter GUI Implementation
class LMSApp:
    def __init__(self):
        self.signup_manager = SignUpManager()
        self.login_manager = LoginManager(self.signup_manager.get_users())
        self.root = tk.Tk()
        self.root.title("Learning Management System")

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_entry = tk.Entry(self.root)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_entry = tk.Entry(self.root, show="*")

        self.login_button = tk.Button(self.root, text="Log In", command=self.login)
        self.signup_button = tk.Button(self.root, text="Sign Up", command=self.signup)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()
        self.signup_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.login_manager.login(username, password):
            self.show_user_menu()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.determine_user_type(username)

        if user_type:
            if self.signup_manager.register_user(username, password, user_type):
                self.show_user_menu()

    def determine_user_type(self, username):
        if username.endswith(".std"):
            return UserType.STUDENT
        elif username.endswith(".ins"):
            return UserType.INSTRUCTOR
        elif username.endswith(".mng"):
            return UserType.MANAGER
        else:
            messagebox.showerror("Error", "Invalid username extension. Sign up failed.")
            return None

    def show_user_menu(self):
        user_type = self.login_manager.get_current_user_type()
        username = self.login_manager.get_current_username()

        messagebox.showinfo("Success", f"{user_type.name} {username} has logged in.")
        
        if user_type == UserType.STUDENT:
            # Create and display the student menu
            student_menu = StudentMenu(self.root)
            student_menu.show_menu()

        elif user_type == UserType.INSTRUCTOR:
            # Create and display the instructor menu
            instructor_menu = InstructorMenu(self.root)
            instructor_menu.show_menu()

        elif user_type == UserType.MANAGER:
            # Create and display the manager menu
            manager_menu = ManagerMenu(self.root)
            manager_menu.show_menu()

        self.root.mainloop()

class StudentMenu:
    def __init__(self, root):
        self.root = root
        self.student_menu = tk.Toplevel(root)
        self.student_menu.title("Student Menu")

        self.view_courses_button = tk.Button(self.student_menu, text="View Enrolled Courses", command=self.view_courses)
        self.view_lectures_button = tk.Button(self.student_menu, text="View Uploaded Lectures", command=self.view_lectures)
        self.logout_button = tk.Button(self.student_menu, text="Logout", command=self.logout)

        self.view_courses_button.pack()
        self.view_lectures_button.pack()
        self.logout_button.pack()

    def view_courses(self):
        # Implement the logic to view enrolled courses
        pass

    def view_lectures(self):
        # Implement the logic to view uploaded lectures
        pass

    def logout(self):
        self.student_menu.destroy()

    def show_menu(self):
        self.root.mainloop()

class InstructorMenu:
    def __init__(self, root):
        self.root = root
        self.instructor_menu = tk.Toplevel(root)
        self.instructor_menu.title("Instructor Menu")

        self.view_quizzes_button = tk.Button(self.instructor_menu, text="View Enrolled Quizzes", command=self.view_quizzes)
        self.add_lecture_button = tk.Button(self.instructor_menu, text="Add Lecture", command=self.add_lecture)
        self.add_quiz_button = tk.Button(self.instructor_menu, text="Add Quiz", command=self.add_quiz)
        self.view_courses_button = tk.Button(self.instructor_menu, text="View Enrolled Courses", command=self.view_courses)
        self.view_lectures_button = tk.Button(self.instructor_menu, text="View Uploaded Lectures", command=self.view_lectures)
        self.logout_button = tk.Button(self.instructor_menu, text="Logout", command=self.logout)

        self.view_quizzes_button.pack()
        self.add_lecture_button.pack()
        self.add_quiz_button.pack()
        self.view_courses_button.pack()
        self.view_lectures_button.pack()
        self.logout_button.pack()


    def add_lecture(self):
        # Implement the logic to add a lecture
        pass


    def view_courses(self):
        # Implement the logic to view enrolled courses
        pass

    def view_lectures(self):
        # Implement the logic to view uploaded lectures
        pass

    def logout(self):
        self.instructor_menu.destroy()

    def show_menu(self):
        self.root.mainloop()

class ManagerMenu:
    def __init__(self, root):
        self.root = root
        self.manager_menu = tk.Toplevel(root)
        self.manager_menu.title("Manager Menu")

        self.add_student_button = tk.Button(self.manager_menu, text="Add Student", command=self.add_student)
        self.add_instructor_button = tk.Button(self.manager_menu, text="Add Instructor", command=self.add_instructor)
        self.add_course_button = tk.Button(self.manager_menu, text="Add Course", command=self.add_course)
        self.modify_student_button = tk.Button(self.manager_menu, text="Modify Student Details", command=self.modify_student)
        self.search_query_button = tk.Button(self.manager_menu, text="Enter search query", command=self.search_query)
        self.enroll_students_button = tk.Button(self.manager_menu, text="Enroll Students to Course", command=self.enroll_students)
        self.display_courses_button = tk.Button(self.manager_menu, text="Display All Courses", command=self.display_courses)
        self.logout_button = tk.Button(self.manager_menu, text="Logout", command=self.logout)

        self.add_student_button.pack()
        self.add_instructor_button.pack()
        self.add_course_button.pack()
        self.modify_student_button.pack()
        self.search_query_button.pack()
        self.enroll_students_button.pack()
        self.display_courses_button.pack()
        self.logout_button.pack()

    def add_student(self):
        # Implement the logic to add a student
        pass

    def add_instructor(self):
        # Implement the logic to add an instructor
        pass

    def add_course(self):
        # Implement the logic to add a course
        pass

    def modify_student(self):
        # Implement the logic to modify student details
        pass

    def search_query(self):
        # Implement the logic for entering a search query
        pass

    def enroll_students(self):
        # Implement the logic to enroll students to a course
        pass

    def display_courses(self):
        # Implement the logic to display all courses
        pass

    def logout(self):
        self.manager_menu.destroy()

    def show_menu(self):
        self.root.mainloop()

if __name__ == "__main__":
    lms_app = LMSApp()
    lms_app.root.mainloop()

