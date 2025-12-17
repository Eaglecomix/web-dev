import tkinter as tk
from tkinter import messagebox
import random
import os

# Define the expected path to the joke file
FILE_PATH = os.path.join("resources", "randomJokes.txt")

class JokeTellerApp:
    def __init__(self, master):
        self.master = master
        master.title("😂 The Daily Joke Box")
        master.geometry("650x350")
        master.minsize(450, 300) 
        master.config(bg='#E8EAEF')
        
        # Configure grid to be responsive (center column expands)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1) 

        # --- Data Loading ---
        self.jokes = self.load_jokes_from_file(FILE_PATH)
        self.current_joke = ("", "") 
        
        # --- GUI Widgets ---
        self.create_widgets()
        self.display_initial_state()

    # --- Data Loading (Functionality Unchanged) ---
    def load_jokes_from_file(self, file_path):
        """Attempts to load jokes from the specified file path."""
        jokes_list = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '?' in line:
                        try:
                            setup, punchline = line.split('?', 1) 
                            jokes_list.append((setup.strip() + '?', punchline.strip()))
                        except ValueError:
                            continue
            if not jokes_list:
                messagebox.showerror("File Error", f"The file '{file_path}' was empty or contained no valid jokes.")
        except FileNotFoundError:
            messagebox.showerror("File Error", f"File not found: Please create the folder 'resources' and place 'randomJokes.txt' inside it.")
        except Exception as e:
            messagebox.showerror("Load Error", f"An unexpected error occurred while reading the file: {e}")
            
        return jokes_list

    # --- Widget Creation (FIXED master reference) ---
    def create_widgets(self):
        # 1. Title/Header Label
        header_label = tk.Label(self.master, 
                                text="Ready for a laugh?", 
                                font=('Segoe UI', 18, 'bold'), 
                                bg='#007BFF', fg='white', pady=10)
        header_label.grid(row=0, column=0, columnspan=3, sticky='ew', padx=0, pady=(0, 15))

        # --- Output Labels Frame ---
        output_frame = tk.Frame(self.master, bg='#F0F0F0', padx=15, pady=15, relief=tk.RIDGE)
        output_frame.grid(row=1, column=0, columnspan=3, sticky='ew', padx=20, pady=10)
        output_frame.grid_columnconfigure(0, weight=1) 

        # 2. Joke Setup Label
        self.setup_label = tk.Label(output_frame, 
                                    font=('Segoe UI', 14, 'italic'), 
                                    bg='#F0F0F0', fg='#333333',
                                    wraplength=600, justify=tk.CENTER)
        self.setup_label.grid(row=0, column=0, pady=(0, 10), sticky='ew')

        # 3. Punchline Label
        self.punchline_label = tk.Label(output_frame, 
                                        text="", 
                                        font=('Segoe UI', 16, 'bold'), 
                                        bg='#F0F0F0', fg='#FF4500', 
                                        wraplength=600, justify=tk.CENTER)
        self.punchline_label.grid(row=1, column=0, pady=(5, 0), sticky='ew')

        # --- Buttons Frame ---
        button_frame = tk.Frame(self.master, bg='#E8EAEF')
        button_frame.grid(row=2, column=0, columnspan=3, pady=(15, 0))

        btn_style = {'font': ('Segoe UI', 10, 'bold'), 'width': 18, 'pady': 5}

        # 4. Joke / Next Button
        self.joke_button = tk.Button(button_frame, 
                                     text="Alexa tell me a Joke", 
                                     command=self.tell_new_joke, 
                                     bg='#28A745', fg='white', 
                                     **btn_style)
        self.joke_button.pack(side=tk.LEFT, padx=10)
        
        # 5. Show Punchline Button
        self.punchline_button = tk.Button(button_frame, 
                                          text="Show Punchline", 
                                          command=self.show_punchline, 
                                          state=tk.DISABLED, 
                                          bg='#FFC107', fg='black', 
                                          **btn_style)
        self.punchline_button.pack(side=tk.LEFT, padx=10)
        
        # 6. Quit Button (FIXED: using self.master instead of just master)
        self.quit_button = tk.Button(self.master, # FIX 1: Container reference
                                     text="Quit Application", 
                                     command=self.master.destroy, # FIX 2: Command reference
                                     bg='#DC3545', fg='white', 
                                     font=('Segoe UI', 10, 'bold'), width=15)
        self.quit_button.grid(row=3, column=1, pady=(25, 10))

    def display_initial_state(self):
        """Sets the initial text based on data loading success."""
        if not self.jokes:
            initial_text = f"ERROR: Could not find or load jokes from '{FILE_PATH}'. 😢"
        else:
            initial_text = "Click 'Alexa tell me a Joke' to begin!"
            
        self.setup_label.config(text=initial_text)

    # --- Functionality Methods (Unchanged) ---
    def tell_new_joke(self):
        """Randomly selects a new joke, displays the setup, and resets the view."""
        if not self.jokes:
            self.setup_label.config(text="No jokes available. Please check the 'randomJokes.txt' file. 🤷‍♀️")
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.punchline_button.config(state=tk.NORMAL)
        
        if self.joke_button['text'] == "Alexa tell me a Joke":
            self.joke_button.config(text="Next Joke")

    def show_punchline(self):
        """Displays the punchline for the current joke."""
        _, punchline = self.current_joke
        if punchline:
            self.punchline_label.config(text=punchline)
            self.punchline_button.config(state=tk.DISABLED)
        else:
            self.punchline_label.config(text="🤔 Error: Click 'Next Joke' first.")

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeTellerApp(root)
    root.mainloop()