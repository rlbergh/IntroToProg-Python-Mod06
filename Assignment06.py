# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Rebecca Bergh,8/5/2024,Modified script, added formatted "Goodbye..." message
#   Rebecca Bergh,8/6/2024,Created classes, functions and did organization
#   Rebecca Bergh,8/7/2024,Removed unnecessary uses of global variables and did some cleaning
# ------------------------------------------------------------------------------------------ #

import json

# Define the Data Constants
MENU: str = '''
——— Course Registration Program ———
  Select from the following menu:  
    1. Register a student for a course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
———————————————————————————————————— 
'''
FILE_NAME: str = "Enrollments.json"
EXIT_MSG: str = '''

    ╔════════════════ « ♦ » ═══╗
             Goodbye...      
    ╚═══ « ♦ » ════════════════╝
'''
# Define the variables
menu_choice: str = ''
students: list = []


class FileProcessor:
    """
    A collection of functions to process the file

    ChangeLog: Who,When,What:
    RBergh,8/6/2024,Created class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        global students
        file = None
        try:
            file = open(FILE_NAME, "r")
            students = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_message('JSON file not found', e)
            print('═'*20)
            print("Creating file since it doesn't exist")
            file = open(file_name, 'w')
            json.dump(students, file)
        except Exception as e:
            IO.output_error_message('Unhandled exception', e)
        finally:
            if not file.closed:
                file.close()
        return students

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        file = None
        try:
            file = open(FILE_NAME, "w")
            json.dump(students, file)
            file.close()
            print("The following data was saved to the file!")
            for student in students:
                print(f'Student {student["FirstName"]} '
                      f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        except Exception as e:
            if not file.closed:
                file.close()
            IO.output_error_message('Unhandled exception', e)


class IO:
    """
    A collection of functions that handle user input

    ChangeLog: Who,When,What
    RBergh,8/6/2024,Created class
    """

    @staticmethod
    def output_error_message(message: str, error: Exception = None):
        print(message)
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_message(message: str):
        print(message)

    @staticmethod
    def input_menu_choice(menu: str) -> str:
        global menu_choice
        menu_choice = input(menu)
        while menu_choice not in ['1', '2', '3', '4']:
            IO.output_message("Please enter either 1, 2, 3 or 4")
            str_choice = input(menu)
        return menu_choice

    @staticmethod
    def input_student_data(student_data: list):
        student_first_name: str = ''  # Holds the first name of a student entered by the user.
        student_last_name: str = ''  # Holds the last name of a student entered by the user.
        course_name: str = ''  # Holds the name of a course entered by the user.
        student_data: dict = {}  # one row of student data

        try:
            # ask for first name until it doesn't contain numbers
            student_first_name = input("Enter the student's first name: ")
            while not student_first_name.isalpha():
                print("The first name should not contain numbers.")
                student_first_name = input("Enter the student's first name again: ")
            # ask for last name until it doesn't contain numbers
            student_last_name = input("Enter the student's last name: ")
            while not student_last_name.isalpha():
                print("The last name should not contain numbers.")
                student_last_name = input("Enter the student's last name again: ")
            # ask for course name
            course_name = input("Please enter the name of the course: ")
            student_data = {"FirstName": student_first_name,
                            "LastName": student_last_name,
                            "CourseName": course_name}
            students.append(student_data)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_message(str(e))
        except Exception as e:
            IO.output_message(str(e))

    @staticmethod
    def output_student_courses(student_data: list):
        print("-" * 50)
        for student in students:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def output_menu(menu: str):
        print(menu)


# MAIN CONTENT
# read data from file
FileProcessor.read_data_from_file(FILE_NAME, students)

# Present and Process the data
while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice('Make a menu selection: ')

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        IO.input_student_data(students)
        continue
    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue
    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(FILE_NAME, students)
        continue
    # Stop the loop
    elif menu_choice == "4":
        print(EXIT_MSG)
        break  # out of the loop
