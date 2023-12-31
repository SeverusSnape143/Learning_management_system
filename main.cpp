#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
enum class UserType { STUDENT, INSTRUCTOR, MANAGER };
template <typename T>
vector<T> readDataFromCSV(const string& filePath) {
    vector<T> data;
    ifstream file(filePath);

    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            istringstream iss(line);
            T obj;
            iss >> obj;
            data.push_back(obj);
        }

        file.close();
    }

    return data;
}

template <typename T>
void writeDataToCSV(const vector<T>& data, const string& filePath) {
    ofstream file(filePath);

    if (file.is_open()) {
        for (const T& obj : data) {
            file << obj << endl;
        }

        file.close();
    }
}



class User {
public:
    string* username;
    string* password;
    UserType type;

    User(const string& uname, const string& pwd, UserType utype)
        : type(utype) {
        username = new string(uname);  
        password = new string(pwd);   
    }
    ~User() {
        delete username;  
        delete password;
    }
};

class SignUpManager {
private:
    vector<User*> users;

public:
    bool registerUser(const string& username, const string& password, UserType userType) {
        for (const User* user : users) {
            if (*(user->username) == username) {
                cout << "Error: Username already exists. Please choose a different username.\n";
                return false;
            }
        }

        users.push_back(new User(username, password, userType));
        cout << "User registered successfully!\n";
        return true;
    }


    const vector<User*>& getUsers() const {
        return users;
    }
};

class LoginManager {
private:
    User* currentUser;
    const vector<User*>& users;

public:
    LoginManager(const vector<User*>& userList) : currentUser(nullptr), users(userList) {}

    bool login(const string& username, const string& password) {
        for (const User* user : users) {
            if (*(user->username) == username && *(user->password) == password) {
                currentUser = new User(*user); 
                cout << "Login successful!\n";
                return true;
            }
        }


        cout << "Login failed. Invalid username or password.\n";
        return false;
    }

    UserType getCurrentUserType() const {
        return isLoggedIn() ? currentUser->type : UserType::STUDENT; 
    }


    bool isLoggedIn() const {
        return currentUser != nullptr;
    }
    string getCurrentUsername() const {
        if (isLoggedIn()) {
            return *(currentUser->username); 
        }
        else {
            return "No user logged in";
        }
    }
    void logout() {
        delete currentUser;
        currentUser = nullptr;
        cout << "Logout successful!\n";
    }
};


class Student {
public:
    string name;
    string fatherName;
    string motherName;
    string address;
    string bloodGroup;
    int rollNumber;
    double grade;

    Student(const string& name, const string& fatherName, const string& motherName,
        const string& address, const string& bloodGroup, int rollNumber, double grade)
        : name(name), fatherName(fatherName), motherName(motherName), address(address),
        bloodGroup(bloodGroup), rollNumber(rollNumber), grade(grade) {}
    Student() : rollNumber(0), grade(0.0) {}

    void saveToFile(ofstream& file) {
        file << name << ","
            << fatherName << ","
            << motherName << ","
            << address << ","
            << bloodGroup << ","
            << rollNumber << ","
            << grade << "\n";
    }

    void modifyDetails() {
        cout << "Enter updated student name: ";
        cin.ignore(); // Ignore newline character in input buffer
        getline(cin, name);

        cout << "Enter updated father's name: ";
        getline(cin, fatherName);

        cout << "Enter updated mother's name: ";
        getline(cin, motherName);

        cout << "Enter updated address: ";
        getline(cin, address);

        cout << "Enter updated blood group: ";
        getline(cin, bloodGroup);

        cout << "Enter updated roll number: ";
        cin >> rollNumber;

        cout << "Enter updated grade: ";
        cin >> grade;
    }

    bool matchesSearchCriteria(const string& searchTerm) {
        // Check if the student's name or roll number contains the search term (case-insensitive)
        string lowerName = name;
        string lowerSearchTerm = searchTerm;
        for (char& c : lowerName) {
            c = tolower(c);
        }
        for (char& c : lowerSearchTerm) {
            c = tolower(c);
        }
        return (lowerName.find(lowerSearchTerm) != string::npos) || (to_string(rollNumber).find(searchTerm) != string::npos);
    }
};

class Instructor {
     
    struct Lecture {
        string courseName;
        string lectureFileName; 

        Lecture(const string& course, const string& filename) : courseName(course), lectureFileName(filename) {}
    };

    vector<Lecture> uploadedLectures;
public:
    string name;
    int CNIC;
    string doj;
    vector<string> enrolledQuizzes; 
    vector<string> enrolledCourses; 

    Instructor(const string& name, int CNIC, const string& doj) : name(name), CNIC(CNIC), doj(doj) {}
    Instructor() :name(""), CNIC(0), doj("") {}

        
        void uploadLecture(string& courseName, string& lectureFilename) {
        uploadedLectures.emplace_back(courseName, lectureFilename);

        
        ofstream lectureFile("lectures_data.csv", ios::app);
        lectureFile << courseName << "," << lectureFilename << endl;
        lectureFile.close();

        cout << "Lecture uploaded successfully for course: " << courseName << endl;
        }
        void viewUploadedLectures() {
            if (uploadedLectures.empty()) {
                cout << "No lectures uploaded."<<endl;
            }
            else {
                cout << "Uploaded Lectures:\n";
                for (const auto& lecture : uploadedLectures) {
                    cout << "Course: " << lecture.courseName << ", File: " << lecture.lectureFileName << endl;
                }
            }
        }

    void saveToFile(ofstream& file) {
        file << name << ","
            << CNIC << ","
            << doj << "\n";
    }
    void modifyDetails() {
        cout << "Enter updated Instructor name: ";
        cin.ignore(); 
        getline(cin, name);

        cout << "Enter updated CNIC: ";
        cin >> CNIC;

        cout << "Enter updated date of joining: ";
        getline(cin, doj);

    }

    bool matchesSearchCriteria(const string& searchTerm) {
    
        string lowerName = name;
        string lowerSearchTerm = searchTerm;
        for (char& c : lowerName) {
            c = tolower(c);
        }
        for (char& c : lowerSearchTerm) {
            c = tolower(c);
        }
        return (lowerName.find(lowerSearchTerm) != string::npos) || (to_string(CNIC).find(searchTerm) != string::npos);
    }
    void viewEnrolledQuizzes() {
        if (enrolledQuizzes.empty()) {
            cout << "No quizzes enrolled."<< endl;
        }
        else {
            cout << "Enrolled Quizzes:"<< endl;
            for (const string& quiz : enrolledQuizzes) {
                cout << quiz << endl;
            }
        }
    }

    void addLecture(const string& courseName) {
        
        cout << "Added a lecture to course: " << courseName << "\n";
    }

    void addQuiz(const string& courseName) {

       cout << "Added a quiz to course: " << courseName << "\n";
    }

    void viewEnrolledCourses() {
        if (enrolledCourses.empty()) {
            cout << "No courses enrolled."<< endl;
        }
        else {
            cout << "Enrolled Courses:\n";
            for (const string& course : enrolledCourses) {
                cout << course << endl;
            }
        }
    }

    void enrollInQuiz(const string& quizName) {
        enrolledQuizzes.push_back(quizName);
        cout << "Enrolled in quiz: " << quizName << endl;
    }

    void enrollInCourse(const string& courseName) {
        enrolledCourses.push_back(courseName);
        cout << "Enrolled in course: " << courseName << endl;
    }
};

class StudentManager {
private:
    vector<Student> students;
    vector<Instructor>instructors;

public:
    void addStudent(const Student& student) {
        students.push_back(student);
    }
    void addInstructor(const Instructor& instructor) {
        instructors.push_back(instructor);
    }
    void setStudents(const vector<Student>& newStudents) {
        students = newStudents;
    }

    void setInstructors(const vector<Instructor>& newInstructors) {
        instructors = newInstructors;
    }

    void saveStudentRecords() {
        ofstream file("student_records.csv", ios::app);

        if (!file) {
            cerr << "Error opening the file for writing." << endl;
            return;
        }

        students.back().saveToFile(file); 

        file.close();
        cout << "Student record added and saved successfully."<< endl;
    }

    void saveInstructorRecords() {
        ofstream file("instructor_records.csv", ios::app); 

        if (!file) {
            cerr << "Error opening the file for writing." << endl;
            return;
        }

        instructors.back().saveToFile(file); 

        file.close();
        cout << "Instructor record added and saved successfully.\n";
    }

    int getStudentCount() {
        return students.size();
    }
    int getInstructorCount() {
        return instructors.size();
    }
    const vector<Student>& getStudents() const {
        return students;
    }

    const vector<Instructor>& getInstructors() const {
        return instructors;
    }
    void modifyStudentDetails(const string& filePath) {
        
        vector<Student> students = readDataFromCSV<Student>("student_records.csv");

        string searchTerm;
        cout << "Enter student name or roll number to modify: ";
        cin.ignore(); 
        getline(cin, searchTerm);

        int index = -1;
        for (int i = 0; i < students.size(); ++i) {
            if (students[i].matchesSearchCriteria(searchTerm)) {
                if (index != -1) {
                    
                    cout << "Error: Multiple students match the search criteria. Please provide a unique name or roll number.\n";
                    return;
                }
                index = i;
            }
        }

        if (index != -1) {
            
            cout << "Student Details:\n";
            cout << "Name: " << students[index].name << "\n";
            cout << "Father's Name: " << students[index].fatherName << "\n";
            cout << "Mother's Name: " << students[index].motherName << "\n";
            cout << "Address: " << students[index].address << "\n";
            cout << "Blood Group: " << students[index].bloodGroup << "\n";
            cout << "Roll Number: " << students[index].rollNumber << "\n";
            cout << "Grade: " << students[index].grade << "\n";

            
            students[index].modifyDetails();

            
            writeDataToCSV(students, "student_records.csv");

            cout << "Student details updated successfully.\n";
        }
        else {
            cout << "No student found with the specified name or roll number.\n";
        }
    }

    void displayAllStudents() {
        for (int i = 0; i < students.size(); i++) {
            cout << "Student " << i + 1 << ":\n";
            cout << "Name: " << students[i].name << "\n";
            cout << "Father's Name: " << students[i].fatherName << "\n";
            cout << "Mother's Name: " << students[i].motherName << "\n";
            cout << "Address: " << students[i].address << "\n";
            cout << "Blood Group: " << students[i].bloodGroup << "\n";
            cout << "Roll Number: " << students[i].rollNumber << "\n";
            cout << "Grade: " << students[i].grade << "\n";
            cout << "\n";
        }
    }

    void searchStudents(const string& searchTerm) {
        vector<int> matchingIndices;
        for (int i = 0; i < students.size(); i++) {
            if (students[i].matchesSearchCriteria(searchTerm)) {
                matchingIndices.push_back(i);
            }
        }

        if (matchingIndices.empty()) {
            cout << "No students found matching the search criteria.\n";
        }
        else {
            cout << "Students matching the search criteria:\n";
            for (int index : matchingIndices) {
                cout << "Student " << index + 1 << ":\n";
                cout << "Name: " << students[index].name << "\n";
                cout << "Father's Name: " << students[index].fatherName << "\n";
                cout << "Mother's Name: " << students[index].motherName << "\n";
                cout << "Address: " << students[index].address << "\n";
                cout << "Blood Group: " << students[index].bloodGroup << "\n";
                cout << "Roll Number: " << students[index].rollNumber << "\n";
                cout << "Grade: " << students[index].grade << "\n";
                cout << "\n";
            }
        }
    }
};


class Course {
public:
    string courseName;
    int courseId;
    int capacity;
    vector<int> enrolledStudents;
    vector<string> uploadedLectures;

    Course(const string& name, int id, int cap)
        : courseName(name), courseId(id), capacity(cap) {}
    Course() : courseId(0), capacity(0) {}

    bool enrollStudent(int studentId) {
        if (enrolledStudents.size() < capacity) {
            enrolledStudents.push_back(studentId);
            return true;
        }
        return false;
    }
    void uploadLecture(const string& lectureName) {
        uploadedLectures.push_back(lectureName);
    }
    const vector<string>& getUploadedLectures() const {
        return uploadedLectures;
    }
};
class CourseManager {
private:

    vector<Course> courses;
    StudentManager& studentManager;


public:
    CourseManager(StudentManager& sm) : studentManager(sm) {};
    const vector<Course>& getCourses() const {
        return courses;
    }
    void addCourse(const Course& course) {
        courses.push_back(course);
    }
    void setCourses(const vector<Course>& newCourses) {
        courses = newCourses;
    }

    void displayAllCourses() {
        for (int i = 0; i < courses.size(); i++) {
            cout << "Course " << i + 1 << ":\n";
            cout << "Name: " << courses[i].courseName << "\n";
            cout << "ID: " << courses[i].courseId << "\n";
            cout << "Capacity: " << courses[i].capacity << "\n";
            cout << "Enrolled Students: " << courses[i].enrolledStudents.size() << "\n";
            cout << "\n";
        }
    }
    void saveCourses() {
        writeDataToCSV(courses, "courses_data.csv");
    }
    bool modifyCourse(int courseId, const Course& updatedCourse) {
        if (courseId >= 1 && courseId <= courses.size()) {
            courses[courseId - 1] = updatedCourse;
            
            return true;
        }
        return false;
    }
    bool enrollStudentInCourse(int studentId, const string& courseName) {
        for (Course& course : courses) {
            if (course.courseName == courseName) {
            
                bool studentAlreadyEnrolled = false;
                for (int enrolledStudentId : course.enrolledStudents) {
                    if (enrolledStudentId == studentId) {
                        studentAlreadyEnrolled = true;
                        break;
                    }
                }

                if (!studentAlreadyEnrolled) {
                    
                    course.enrolledStudents.push_back(studentId);

                    
                    ofstream enrolledFile("enrolled_students.csv", ios::app);
                    enrolledFile << courseName << "," << studentId << "\n";
                    enrolledFile.close();

                    
                    ofstream coursesFile("courses_data.csv");
                    for (const Course& c : courses) {
                        coursesFile << c.courseName << "," << c.capacity << "," << c.enrolledStudents.size() << "\n";
                    }
                    coursesFile.close();

                    cout << "Student enrolled successfully in the course!\n";
                    return true;
                }
                else {
                    cout << "Error: Student is already enrolled in the course.\n";
                }
                break;
            }
        }

        cout << "Error: Course not found.\n";
        return false;
    }

    void enrollStudentInCourse(CourseManager& courseManager, int studentId, const string& courseName) {
        courseManager.enrollStudentInCourse(studentId, courseName);
    }
};
istream& operator>>(istream& is, Student& student) {
    char comma;
    return is >> student.name >> comma
        >> student.fatherName >> comma
        >> student.motherName >> comma
        >> student.address >> comma
        >> student.bloodGroup >> comma
        >> student.rollNumber >> comma
        >> student.grade;
}

ostream& operator<<(ostream& os, const Student& student) {
    return os << student.name << ","
        << student.fatherName << ","
        << student.motherName << ","
        << student.address << ","
        << student.bloodGroup << ","
        << student.rollNumber << ","
        << student.grade;
}


istream& operator>>(istream& is, Instructor& instructor) {
    char comma;
    return is >> instructor.name >> comma
        >> instructor.CNIC >> comma
        >> instructor.doj;
}

ostream& operator<<(ostream& os, const Instructor& instructor) {
    return os << instructor.name << ","
        << instructor.CNIC << ","
        << instructor.doj;
}


istream& operator>>(istream& is, Course& course) {
    char comma;
    return is >> course.courseName >> comma
        >> course.courseId >> comma
        >> course.capacity;
}

ostream& operator<<(ostream& os, const Course& course) {
    return os << course.courseName << ","
        << course.courseId << ","
        << course.capacity;
}
int main() {
    SignUpManager signUpManager;
    LoginManager loginManager(signUpManager.getUsers());
    StudentManager studentManager;
    CourseManager courseManager(studentManager);
    Instructor instructor;
    int choice;
    ::string username, password, name, fatherName, motherName, address, bloodGroup, searchTerm, addcourse, doj;
    int rollNumber, CNIC;
    double grade;

    
    studentManager.setStudents(readDataFromCSV<Student>("students_records.csv"));
    studentManager.setInstructors(readDataFromCSV<Instructor>("instructor_data.csv"));
    courseManager.setCourses(readDataFromCSV<Course>("courses_data.csv"));
    while (true) {
        cout << "Welcome to Learning Management System" << endl;
        cout << "1) Sign Up\n2) Log In\n";
        cin >> choice;

        if (choice == 1) {
            
            cout << "Enter username (with extension .std, .ins, or .mng): ";
            cin >> username;

            cout << "Enter password: ";
            cin >> password;

            UserType type;
            if (username.find(".std") != string::npos) {
                type = UserType::STUDENT;
            }
            else if (username.find(".ins") != string::npos) {
                type = UserType::INSTRUCTOR;
            }
            else if (username.find(".mng") != string::npos) {
                type = UserType::MANAGER;
            }
            else {
                cout << "Invalid username extension. Sign up failed.\n";
                continue;
            }

            signUpManager.registerUser(username, password, type);

        }
        if (choice == 1) {
        
            cout << "Enter username (with extension .std, .ins, or .mng): ";
            cin >> username;

            cout << "Enter password: ";
            cin >> password;
            UserType type;
            if (username.find(".std") != string::npos) {
                type = UserType::STUDENT;
            }
            else if (username.find(".ins") != string::npos) {
                type = UserType::INSTRUCTOR;
            }
            else if (username.find(".mng") != string::npos) {
                type = UserType::MANAGER;
            }
            else {
                cout << "Invalid username extension. Sign up failed.\n";
                continue;
            }

            signUpManager.registerUser(username, password, type);
        }
        else if (choice == 2) {
            cout << "Enter username: ";
            cin >> username;

            cout << "Enter password: ";
            cin >> password;

            if (loginManager.login(username, password)) {
                switch (loginManager.getCurrentUserType()) {
                case UserType::STUDENT: {
                    cout << "Student " << loginManager.getCurrentUsername() << " has logged in.\n";
                    while (true) {
                        cout << "\nStudent Menu:\n";
                        cout << "1) View Enrolled Courses\n2) View Uploaded Lectures\n3) Logout\n";
                        cin >> choice;

                        if (choice == 1) {
                            courseManager.displayAllCourses();
                        }
                        else if (choice == 2) {
                            string courseName;
                            cout << "Enter course name to view lectures: ";
                            cin.ignore(); 
                            getline(cin, courseName);

                            
                            bool courseFound = false;
                            for (const Course& course : courseManager.getCourses()) {
                                if (course.courseName == courseName) {
                                    courseFound = true;
                                    
                                    
                                    vector<string> lectures = course.getUploadedLectures();

                                    if (lectures.empty()) {
                                        cout << "No lectures uploaded for this course.\n";
                                    }
                                    else {
                                        cout << "Uploaded Lectures for " << courseName << ":\n";
                                        for (const string& lecture : lectures) {
                                            cout << lecture << "\n";
                                        }
                                    }
                                    break;
                                }
                            }
                            if (!courseFound) {
                                cout << "Course not found.\n";
                            }
                        }
                        else if (choice == 3) {
                            loginManager.logout();
                            break;
                        }
                        else {
                            cout << "Invalid choice.\n";
                        }
                    }
                    break;
                }
                
                case UserType::INSTRUCTOR: {
                    cout << "Instructor " << loginManager.getCurrentUsername() << " has logged in.\n";
                    while (true) {
                        cout << "\nInstructor Menu:\n";
                        cout << "1) View Enrolled Quizzes\n2) Add Lecture\n3) Add Quiz\n4) View Enrolled Courses\n5) View Uploaded Lectures\n6) Logout\n";
                        cin >> choice;

                        if (choice == 1) {
                            instructor.viewEnrolledQuizzes();
                        }
                        else if (choice == 2) {
                            string courseName, lectureFileName;
                            cout << "Enter course name to add lecture: ";
                            cin.ignore(); 
                            getline(cin, courseName);

                            cout << "Enter file name of the lecture (PDF, etc.): ";
                            getline(cin, lectureFileName);

                            
                            instructor.uploadLecture(courseName, lectureFileName);
                        }
                        else if (choice == 3) {
                            string courseName;
                            cout << "Enter course name to add quiz: ";
                            cin.ignore(); 
                            getline(cin, courseName);
                            instructor.addQuiz(courseName);
                        }
                        else if (choice == 4) {
                            instructor.viewEnrolledCourses();
                        }
                        else if (choice == 5) {
                            instructor.viewUploadedLectures();
                        }
                        else if (choice == 6) {
                            loginManager.logout();
                            break;
                        }
                        else {
                            cout << "Invalid choice.\n";
                        }
                    }
                    break;
                }
                case UserType::MANAGER: {
                    cout << "Manager " << loginManager.getCurrentUsername() << " has logged in.\n";
                    while (true) {
                        cout << "\nManager Menu:\n";
                        cout << "1) Add Student\n2) Add Instructor\n3) Add Course\n4) Modify Student Details\n5) Enter search query\n6) Enroll Students to course\n7) Display all courses\n8) Logout \n";
                        cin >> choice;

                        if (choice == 1) {
                            cout << "Enter student name: ";
                            cin.ignore();
                            
                            getline(cin, name);

                            cout << "Enter father's name: ";
                            getline(cin, fatherName);

                            cout << "Enter mother's name: ";
                            getline(cin, motherName);

                            cout << "Enter address: ";
                            getline(cin, address);

                            cout << "Enter blood group: ";
                            getline(cin, bloodGroup);

                            cout << "Enter roll number: ";
                            cin >> rollNumber;

                            cout << "Enter grade: ";
                            cin >> grade;

                            studentManager.addStudent(Student(name, fatherName, motherName, address, bloodGroup, rollNumber, grade));
                            studentManager.saveStudentRecords();
                        }
                        else if (choice == 2) {
                            cout << "Enter instructor name: ";
                            cin.ignore();
                            getline(cin, name);

                            cout << "Enter CNIC number: ";
                            cin >> CNIC;

                            cout << "Enter Date of Joining (DD-MM-YYYY): ";
                            cin.ignore();
                            getline(cin, doj);

                            studentManager.addInstructor(Instructor(name, CNIC, doj));
                            studentManager.saveInstructorRecords();


                            
                            
                        }
                        else if (choice == 3) {
                            
                            string courseName;
                            int courseId, capacity;

                            cout << "Enter course name: ";
                            cin.ignore();
                            getline(cin, courseName);

                            cout << "Enter course ID: ";
                            cin >> courseId;

                            cout << "Enter course capacity: ";
                            cin >> capacity;

                            courseManager.addCourse(Course(courseName, courseId, capacity));
                            writeDataToCSV(courseManager.getCourses(), "courses_data.csv");
                            cout << "New course has been added to lms!\n";
                        }
                        else if (choice == 4) {
                            
                            cout << "Enter student name or roll number to modify: ";
                            cin.ignore(); 
                            getline(cin, searchTerm);
                            studentManager.modifyStudentDetails(searchTerm);
                        }
                        else if (choice == 5) {
                            
                            cout << "Enter a search query: ";
                            cin.ignore();
                            getline(cin, searchTerm);
                            studentManager.searchStudents(searchTerm);
                        }
                        else if (choice == 6) {
                            
                            int studentId;
                            string courseName;
                            cout << "Enter student ID to enroll: ";
                            cin >> studentId;

                            cout << "Enter course name to enroll in: ";
                            cin.ignore();
                            getline(cin, courseName);

                            courseManager.enrollStudentInCourse(studentId, courseName);
                        }

                        else if (choice == 7) {
                            courseManager.displayAllCourses();
                        }
                        else if (choice == 8) {
                            loginManager.logout();
                            break;
                        }
                        else {
                            cout << "Invalid choice.\n";
                        }
                    }
                    break;
                }
                default:
                    break;
                }
            }
            writeDataToCSV(studentManager.getStudents(), "student_data.csv");
            writeDataToCSV(studentManager.getInstructors(), "instructor_record.csv");
            writeDataToCSV(courseManager.getCourses(), "courses_data.csv");
        }

    }

    return 0;
}