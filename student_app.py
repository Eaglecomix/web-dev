import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import os
import sys

# Define the expected path to the student marks file
FILE_PATH = os.path.join("resources", "studentMarks.txt")

# --- Data Structure for Students ---
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = code
        self.name = name
        self.c1 = int(c1)
        self.c2 = int(c2)
        self.c3 = int(c3)
        self.exam = int(exam)
        
        self.coursework_total = self.c1 + self.c2 + self.c3 
        self.overall_total = self.coursework_total + self.exam 
        self.percentage = (self.overall_total / 160) * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.percentage >= 70:
            return 'A'
        elif 60 <= self.percentage < 70:
            return 'B'
        elif 50 <= self.percentage < 60:
            return 'C'
        elif 40 <= self.percentage < 50:
            return 'D'
        else:
            return 'F'

    def format_details(self):
        return (
            f"Student Name: {self.name}\n"
            f"Student Number: {self.code}\n"
            f"Coursework Total: {self.coursework_total} / 60\n"
            f"Exam Mark: {self.exam} / 100\n"
            f"Overall Percentage: {self.percentage:.2f}%\n"
            f"Student Grade: {self.grade}\n"
            f"{'-' * 40}"
        )


class StudentApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Marks Analyser 📊")
        master.geometry("800x600")
        master.config(bg='#f0f0f0')
        
        # Configure the main window grid: Column 0 expands, Row 2 expands
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(2, weight=1) 

        # --- Data Storage ---
        self.students = self.load_data()
        self.num_students = len(self.students)
        
        # --- GUI Elements ---
        self.create_title_label()
        self.create_button_bar() 
        self.create_output_area() 
        self.display_welcome()

    # --- Data Loading and Parsing (Unchanged) ---
    def load_data(self):
        students_list = []
        data_lines = []
        
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                data_lines = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("File Not Found", 
                                   f"FATAL ERROR: The required file '{FILE_PATH}' was not found. Exiting.")
            sys.exit() 
        except Exception as e:
            messagebox.showerror("Loading Error", f"An error occurred while reading the file: {e}")
            sys.exit()

        if not data_lines:
            messagebox.showwarning("Empty File", f"The file '{FILE_PATH}' is empty.")
            return []

        for line in data_lines[1:]:
            parts = line.strip().split(',')
            if len(parts) == 6:
                try:
                    code, name, c1, c2, c3, exam = parts
                    students_list.append(Student(code.strip(), name.strip(), c1, c2, c3, exam))
                except ValueError:
                    continue
        
        try:
            expected_count = int(data_lines[0].strip())
            if len(students_list) != expected_count:
                 messagebox.showwarning("Data Mismatch", 
                                    f"WARNING: File header specified {expected_count} students, but only {len(students_list)} valid records were loaded.")
        except ValueError:
            messagebox.showwarning("Header Error", "WARNING: Could not parse the student count from the first line of the file.")

        return students_list

    # --- GUI Setup with Buttons and Labels ---
    def create_title_label(self):
        """Creates a descriptive title label."""
        title_label = tk.Label(self.master, text="Student Data Analysis Console",
                               font=('Arial', 16, 'bold'), bg='#1E90FF', fg='white', pady=10)
        title_label.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))

    def create_button_bar(self):
        """Creates the frame and buttons for management actions."""
        button_bar = tk.Frame(self.master, bg='#f0f0f0', padx=10, pady=5)
        button_bar.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        
        for i in range(5): 
            button_bar.grid_columnconfigure(i, weight=1)

        btn_style = {'font': ('Arial', 10, 'bold'), 'width': 18, 'pady': 5}

        # 1. View All
        btn_all = tk.Button(button_bar, text="1. View All", command=self.view_all_records,
                            bg='#4CAF50', fg='white', **btn_style)
        btn_all.grid(row=0, column=0, padx=5, sticky='ew')

        # 2. View Individual
        btn_individual = tk.Button(button_bar, text="2. View Individual", command=self.view_individual_record,
                                   bg='#2196F3', fg='white', **btn_style)
        btn_individual.grid(row=0, column=1, padx=5, sticky='ew')

        # 3. Highest Score
        btn_highest = tk.Button(button_bar, text="3. Highest Score", command=self.show_highest_score,
                                bg='#FFC107', fg='black', **btn_style)
        btn_highest.grid(row=0, column=2, padx=5, sticky='ew')

        # 4. Lowest Score
        btn_lowest = tk.Button(button_bar, text="4. Lowest Score", command=self.show_lowest_score,
                                bg='#FF9800', fg='black', **btn_style)
        btn_lowest.grid(row=0, column=3, padx=5, sticky='ew')

        # Quit Button
        btn_quit = tk.Button(button_bar, text="QUIT", command=self.master.destroy,
                             bg='#F44336', fg='white', **btn_style)
        btn_quit.grid(row=0, column=4, padx=5, sticky='ew')


    def create_output_area(self):
        """Creates the main scrolled text area for displaying output."""
        output_frame = tk.Frame(self.master, padx=10, pady=5, bg='#ffffff')
        output_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        
        self.output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10), 
                                                     bg='#EAEAEA', fg='#333333', 
                                                     padx=5, pady=5)
        self.output_area.pack(fill='both', expand=True)
        self.output_area.config(state=tk.DISABLED)

    def display_output(self, text):
        """Helper to safely insert text into the output area."""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state=tk.DISABLED)

    def display_welcome(self):
        """Displays a welcome message on startup."""
        if not self.students:
            self.display_output(
                "No student records were loaded. Please check that the file is correctly placed in 'resources/studentMarks.txt'."
            )
            return
            
        self.display_output(
            "Welcome to the Student Marks Analyser!\n"
            "--------------------------------------\n"
            f"Successfully loaded {self.num_students} student records.\n\n"
            "Use the buttons above to perform an action."
        )

    # --- Functionality Methods (Unchanged) ---
    def view_all_records(self):
        if not self.students:
            self.display_output("No student data available to view.")
            return

        all_details = "--- ALL STUDENT RECORDS ---\n"
        total_percentage_sum = 0
        
        for student in self.students:
            all_details += student.format_details()
            total_percentage_sum += student.percentage

        average_percentage = total_percentage_sum / self.num_students if self.num_students > 0 else 0

        summary = (
            "\n--- CLASS SUMMARY ---\n"
            f"Number of Students in Class: {self.num_students}\n"
            f"Average Percentage Mark Obtained: {average_percentage:.2f}%\n"
            "---------------------"
        )
        
        self.display_output(all_details + summary)

    def view_individual_record(self):
        if not self.students:
            self.display_output("No student data available.")
            return

        search_term = simpledialog.askstring("Search Student", "Enter Student Code or Name:", 
                                             parent=self.master)
        
        if not search_term:
            return

        search_term = search_term.strip().lower()
        found_student = None

        for student in self.students:
            if student.code == search_term or student.name.lower() == search_term:
                found_student = student
                break
        
        if found_student:
            output = f"--- INDIVIDUAL STUDENT RECORD ---\n{found_student.format_details()}"
        else:
            output = f"Error: Student with code or name '{search_term}' not found."
            
        self.display_output(output)

    def show_highest_score(self):
        if not self.students:
            self.display_output("No student data available to analyse.")
            return

        highest_student = max(self.students, key=lambda s: s.overall_total)

        output = (
            "--- STUDENT WITH HIGHEST TOTAL SCORE ---\n"
            f"Highest Score: {highest_student.overall_total} / 160\n"
            f"{'-' * 40}\n"
            f"{highest_student.format_details()}"
        )
        self.display_output(output)

    def show_lowest_score(self):
        if not self.students:
            self.display_output("No student data available to analyse.")
            return

        lowest_student = min(self.students, key=lambda s: s.overall_total)

        output = (
            "--- STUDENT WITH LOWEST TOTAL SCORE ---\n"
            f"Lowest Score: {lowest_student.overall_total} / 160\n"
            f"{'-' * 40}\n"
            f"{lowest_student.format_details()}"
        )
        self.display_output(output)

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()