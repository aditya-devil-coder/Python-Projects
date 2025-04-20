import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import csv
import os

class Student:
    
    def __init__(self, student_id, name, age, grade_level, email=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade_level = grade_level
        self.email = email
        self.courses = {}  # Dictionary to store course: marks
        
    def add_course(self, course, marks):
        self.courses[course] = marks
        
    def remove_course(self, course):
        """Remove a course"""
        if course in self.courses:
            del self.courses[course]
            return True
        return False
    
    def calculate_gpa(self):
        if not self.courses:
            return 0.0
            
        total_points = 0
        for course, marks in self.courses.items():
            # Convert percentage to 4.0 scale
            if marks >= 90:
                points = 4.0  # A
            elif marks >= 80:
                points = 3.0  # B
            elif marks >= 70:
                points = 2.0  # C
            elif marks >= 60:
                points = 1.0  # D
            else:
                points = 0.0  # F
            total_points += points
            
        return round(total_points / len(self.courses), 2)
    
    def get_grade(self, course):
        
        if course not in self.courses:
            return "N/A"
        
        marks = self.courses[course]
        if marks >= 90:
            return "A"
        elif marks >= 80:
            return "B"
        elif marks >= 70:
            return "C"
        elif marks >= 60:
            return "D"
        else:
            return "F"
    
    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade Level: {self.grade_level}"

class StudentInformationSystem:
    
    
    def __init__(self):
        self.students = {}  # Dictionary to store student_id: Student object
        self.courses = set()  # Set to track all available courses
        
    def add_student(self, student_id, name, age, grade_level, email=None):
        
        if student_id in self.students:
            print(f"Student with ID {student_id} already exists.")
            return False
        
        self.students[student_id] = Student(student_id, name, age, grade_level, email)
        print(f"Student {name} added successfully with ID {student_id}.")
        return True
        
    def update_student(self, student_id, **kwargs):
    
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return False
        
        student = self.students[student_id]
        
        for key, value in kwargs.items():
            if key in ['name', 'age', 'grade_level', 'email']:
                setattr(student, key, value)
                
        print(f"Student with ID {student_id} updated successfully.")
        return True
        
    def delete_student(self, student_id):
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return False
        
        del self.students[student_id]
        print(f"Student with ID {student_id} deleted successfully.")
        return True
        
    def get_student(self, student_id):
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return None
        
        return self.students[student_id]
        
    def list_all_students(self):
        
        if not self.students:
            print("No students in the system.")
            return pd.DataFrame()
        
        student_data = []
        for student in self.students.values():
            gpa = student.calculate_gpa()
            student_info = {
                'ID': student.student_id,
                'Name': student.name,
                'Age': student.age,
                'Grade Level': student.grade_level,
                'Email': student.email,
                'GPA': gpa
            }
            student_data.append(student_info)
            
        return pd.DataFrame(student_data)
        
    def add_course_marks(self, student_id, course, marks):
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return False
        
        student = self.students[student_id]
        student.add_course(course, marks)
        self.courses.add(course)
        print(f"Marks for {course} added/updated for student {student.name}.")
        return True
        
    def remove_course(self, student_id, course):
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found.")
            return False
        
        student = self.students[student_id]
        if student.remove_course(course):
            print(f"Course {course} removed for student {student.name}.")
            return True
        else:
            print(f"Course {course} not found for student {student.name}.")
            return False
            
    def get_performance_summary(self, student_id=None):
    
        if student_id:
            if student_id not in self.students:
                print(f"Student with ID {student_id} not found.")
                return None
            
            student = self.students[student_id]
            if not student.courses:
                print(f"No courses found for student {student.name}.")
                return None
                
            course_data = []
            for course, marks in student.courses.items():
                course_data.append({
                    'Course': course,
                    'Marks': marks,
                    'Grade': student.get_grade(course)
                })
                
            return pd.DataFrame(course_data)
        else:
            
            if not self.students:
                print("No students in the system.")
                return None
                
            all_data = []
            for student in self.students.values():
                for course, marks in student.courses.items():
                    all_data.append({
                        'Student ID': student.student_id,
                        'Name': student.name,
                        'Course': course,
                        'Marks': marks,
                        'Grade': student.get_grade(course)
                    })
                    
            if not all_data:
                print("No course data found for any student.")
                return None
                
            return pd.DataFrame(all_data)
            
    def find_class_topper(self, course=None):
        
        if not self.students:
            print("No students in the system.")
            return None
            
        if course:
            course_students = []
            for student in self.students.values():
                if course in student.courses:
                    course_students.append((student, student.courses[course]))
                    
            if not course_students:
                print(f"No students found for course {course}.")
                return None
                
            topper = max(course_students, key=lambda x: x[1])
            print(f"Class topper for {course}: {topper[0].name} with marks {topper[1]}")
            
            return {
                'Student ID': topper[0].student_id,
                'Name': topper[0].name,
                'Marks': topper[1],
                'Grade': topper[0].get_grade(course)
            }
        else:
            gpa_students = []
            for student in self.students.values():
                gpa = student.calculate_gpa()
                gpa_students.append((student, gpa))
                
            if not gpa_students:
                print("No GPA data available.")
                return None
                
            topper = max(gpa_students, key=lambda x: x[1])
            print(f"Overall topper: {topper[0].name} with GPA {topper[1]}")
            
            return {
                'Student ID': topper[0].student_id,
                'Name': topper[0].name,
                'GPA': topper[1]
            }
            
    def visualize_performance(self, course=None):
        plt.figure(figsize=(12, 6))
        
        if course:
            # Visualize performance for a specific course
            course_data = []
            for student in self.students.values():
                if course in student.courses:
                    course_data.append({
                        'Student': student.name,
                        'Marks': student.courses[course]
                    })
                    
            if not course_data:
                print(f"No data available for course {course}.")
                return
                
            course_df = pd.DataFrame(course_data)
            plt.bar(course_df['Student'], course_df['Marks'], color='skyblue')
            plt.xlabel('Students')
            plt.ylabel('Marks')
            plt.title(f'Student Performance in {course}')
            plt.xticks(rotation=45)
            plt.ylim(0, 100)
            
            for i, v in enumerate(course_df['Marks']):
                plt.text(i, v + 2, str(v), ha='center')
                
            plt.tight_layout()
            plt.show()
        else:
            # Visualize overall GPA
            gpa_data = []
            for student in self.students.values():
                gpa = student.calculate_gpa()
                gpa_data.append({
                    'Student': student.name,
                    'GPA': gpa
                })
                
            if not gpa_data:
                print("No GPA data available.")
                return
                
            gpa_df = pd.DataFrame(gpa_data)
            plt.bar(gpa_df['Student'], gpa_df['GPA'], color='lightgreen')
            plt.xlabel('Students')
            plt.ylabel('GPA')
            plt.title('Student GPA Comparison')
            plt.xticks(rotation=45)
            plt.ylim(0, 4.0)
            
            for i, v in enumerate(gpa_df['GPA']):
                plt.text(i, v + 0.1, str(v), ha='center')
                
            plt.tight_layout()
            plt.show()
            
    def export_to_csv(self, filename='student_data.csv'):
        if not self.students:
            print("No students in the system to export.")
            return False
            
        try:
            with open(filename, 'w', newline='') as csvfile:
                # Write students basic info
                writer = csv.writer(csvfile)
                writer.writerow(['Student ID', 'Name', 'Age', 'Grade Level', 'Email', 'GPA', 'Course', 'Marks', 'Grade'])
                
                for student in self.students.values():
                    gpa = student.calculate_gpa()
                    if student.courses:
                        for course, marks in student.courses.items():
                            writer.writerow([
                                student.student_id,
                                student.name,
                                student.age,
                                student.grade_level,
                                student.email,
                                gpa,
                                course,
                                marks,
                                student.get_grade(course)
                            ])
                    else:
                        writer.writerow([
                            student.student_id,
                            student.name,
                            student.age,
                            student.grade_level,
                            student.email,
                            gpa,
                            '', '', ''
                        ])
                        
            print(f"Data exported successfully to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
            
    def import_from_csv(self, filename='student_data.csv'):
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return False
            
        try:
        
            self.students = {}
            self.courses = set()
            
            df = pd.read_csv(filename)
            processed_students = set()
            
            for _, row in df.iterrows():
                student_id = row['Student ID']
                if student_id not in processed_students:
                    self.add_student(
                        student_id,
                        row['Name'],
                        row['Age'],
                        row['Grade Level'],
                        row['Email'] if 'Email' in row and not pd.isna(row['Email']) else None
                    )
                    processed_students.add(student_id)
                
                if 'Course' in row and not pd.isna(row['Course']) and row['Course'] != '':
                    self.add_course_marks(student_id, row['Course'], row['Marks'])
                    
            print(f"Data imported successfully from {filename}")
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False

sis = StudentInformationSystem()


def demo_initialize_data():
    sis.add_student(1001, "John Smith", 18, "12th", "john@example.com")
    sis.add_student(1002, "Emma Johnson", 17, "11th", "emma@example.com")
    sis.add_student(1003, "Michael Brown", 18, "12th", "michael@example.com")
    sis.add_student(1004, "Olivia Davis", 17, "11th", "olivia@example.com")
    sis.add_student(1005, "William Wilson", 16, "10th", "william@example.com")
    
    # Add course marks
    sis.add_course_marks(1001, "Mathematics", 92)
    sis.add_course_marks(1001, "Physics", 88)
    sis.add_course_marks(1001, "Chemistry", 78)
    
    sis.add_course_marks(1002, "Mathematics", 95)
    sis.add_course_marks(1002, "Biology", 90)
    sis.add_course_marks(1002, "Chemistry", 82)
    
    sis.add_course_marks(1003, "Mathematics", 75)
    sis.add_course_marks(1003, "Physics", 80)
    sis.add_course_marks(1003, "Computer Science", 98)
    
    sis.add_course_marks(1004, "Mathematics", 88)
    sis.add_course_marks(1004, "Biology", 92)
    sis.add_course_marks(1004, "Chemistry", 85)
    
    sis.add_course_marks(1005, "Mathematics", 78)
    sis.add_course_marks(1005, "Physics", 65)
    sis.add_course_marks(1005, "Chemistry", 72)
    
    print("Sample data initialized successfully")

def menu():
    print("\n" + "="*50)
    print("\tSTUDENT INFORMATION SYSTEM")
    print("="*50)
    print("1. Add a new student")
    print("2. Update student information")
    print("3. Delete a student")
    print("4. List all students")
    print("5. Add/Update course marks")
    print("6. View student performance")
    print("7. Find class topper")
    print("8. Visualize performance")
    print("9. Export data to CSV")
    print("10. Import data from CSV")
    print("11. Initialize sample data")
    print("0. Exit")
    print("="*50)
    
    choice = input("Enter your choice: ")
    return choice

def add_student_ui():
    print("\n--- Add a New Student ---")
    
    student_id = input("Enter Student ID: ")
    try:
        student_id = int(student_id)
    except ValueError:
        print("Student ID should be a number.")
        return
    
    name = input("Enter Name: ")
    
    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Age should be a number.")
        return
    
    grade_level = input("Enter Grade Level: ")
    email = input("Enter Email (optional): ")
    
    if email.strip() == "":
        email = None
    
    sis.add_student(student_id, name, age, grade_level, email)

def update_student_ui():
    print("\n--- Update Student Information ---")
    
    try:
        student_id = int(input("Enter Student ID to update: "))
    except ValueError:
        print("Student ID should be a number.")
        return
    
    student = sis.get_student(student_id)
    if not student:
        return
    
    print(f"Updating information for: {student.name}")
    print("Leave blank to keep the current value.")
    
    name = input(f"Enter Name [{student.name}]: ")
    age_str = input(f"Enter Age [{student.age}]: ")
    grade_level = input(f"Enter Grade Level [{student.grade_level}]: ")
    email = input(f"Enter Email [{student.email}]: ")
    
    update_data = {}
    if name:
        update_data['name'] = name
    if age_str:
        try:
            update_data['age'] = int(age_str)
        except ValueError:
            print("Age should be a number.")
    if grade_level:
        update_data['grade_level'] = grade_level
    if email:
        update_data['email'] = email
        
    sis.update_student(student_id, **update_data)

def delete_student_ui():
    print("\n--- Delete a Student ---")
    
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Student ID should be a number.")
        return
    
    confirm = input(f"Are you sure you want to delete student with ID {student_id}? (y/n): ")
    if confirm.lower() == 'y':
        sis.delete_student(student_id)

def add_course_marks_ui():
    print("\n--- Add/Update Course Marks ---")
    
    try:
        student_id = int(input("Enter Student ID: "))
    except ValueError:
        print("Student ID should be a number.")
        return
    
    student = sis.get_student(student_id)
    if not student:
        return
    
    print(f"Adding marks for: {student.name}")
    
    course = input("Enter Course Name: ")
    
    try:
        marks = float(input("Enter Marks (0-100): "))
        if marks < 0 or marks > 100:
            print("Marks should be between 0 and 100.")
            return
    except ValueError:
        print("Marks should be a number.")
        return
    
    sis.add_course_marks(student_id, course, marks)

def view_performance_ui():
    print("\n--- View Student Performance ---")
    
    choice = input("View performance for (1) individual student or (2) all students? (1/2): ")
    
    if choice == '1':
        try:
            student_id = int(input("Enter Student ID: "))
        except ValueError:
            print("Student ID should be a number.")
            return
            
        student = sis.get_student(student_id)
        if not student:
            return
            
        print(f"\nPerformance Summary for {student.name}:")
        print(f"GPA: {student.calculate_gpa()}")
        
        summary = sis.get_performance_summary(student_id)
        if summary is not None:
            display(summary)
    else:
        print("\nPerformance Summary for All Students:")
        summary = sis.get_performance_summary()
        if summary is not None:
            display(summary)

def find_topper_ui():
    print("\n--- Find Class Topper ---")
    
    choice = input("Find topper for (1) specific course or (2) overall? (1/2): ")
    
    if choice == '1':
        print("Available courses:")
        for course in sorted(sis.courses):
            print(f"- {course}")
            
        course = input("\nEnter Course Name: ")
        if course not in sis.courses:
            print(f"Course {course} not found.")
            return
            
        topper = sis.find_class_topper(course)
        if topper:
            print(f"\nTopper for {course}:")
            print(f"Name: {topper['Name']}")
            print(f"Marks: {topper['Marks']}")
            print(f"Grade: {topper['Grade']}")
    else:
        topper = sis.find_class_topper()
        if topper:
            print("\nOverall Topper:")
            print(f"Name: {topper['Name']}")
            print(f"GPA: {topper['GPA']}")

def visualize_ui():
    print("\n--- Visualize Performance ---")
    
    choice = input("Visualize (1) specific course or (2) overall GPA? (1/2): ")
    
    if choice == '1':
        print("Available courses:")
        for course in sorted(sis.courses):
            print(f"- {course}")
            
        course = input("\nEnter Course Name: ")
        if course not in sis.courses:
            print(f"Course {course} not found.")
            return
            
        sis.visualize_performance(course)
    else:
        sis.visualize_performance()

def export_data_ui():
    print("\n--- Export Data to CSV ---")
    
    filename = input("Enter filename (default: student_data.csv): ")
    if not filename:
        filename = 'student_data.csv'
        
    if not filename.endswith('.csv'):
        filename += '.csv'
        
    sis.export_to_csv(filename)

def import_data_ui():
    print("\n--- Import Data from CSV ---")
    
    filename = input("Enter filename (default: student_data.csv): ")
    if not filename:
        filename = 'student_data.csv'
        
    if not filename.endswith('.csv'):
        filename += '.csv'
        
    confirm = input("This will overwrite all current data. Continue? (y/n): ")
    if confirm.lower() == 'y':
        sis.import_from_csv(filename)

def run_sis():
    while True:
        choice = menu()
        
        if choice == '0':
            print("\nExiting Student Information System. Goodbye!")
            break
        elif choice == '1':
            add_student_ui()
        elif choice == '2':
            update_student_ui()
        elif choice == '3':
            delete_student_ui()
        elif choice == '4':
            print("\n--- List of All Students ---")
            students_df = sis.list_all_students()
            if not students_df.empty:
                display(students_df)
        elif choice == '5':
            add_course_marks_ui()
        elif choice == '6':
            view_performance_ui()
        elif choice == '7':
            find_topper_ui()
        elif choice == '8':
            visualize_ui()
        elif choice == '9':
            export_data_ui()
        elif choice == '10':
            import_data_ui()
        elif choice == '11':
            demo_initialize_data()
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        clear_output(wait=True)

# Uncomment to run the system
run_sis()
