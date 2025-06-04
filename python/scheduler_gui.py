import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from python.scheduler import Scheduler, Shift
import csv
import os

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Schedule Manager")
        self.scheduler = Scheduler()
        
        # Configure the main window
        self.root.geometry("800x600")
        self.root.configure(padx=20, pady=20)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu
        self.create_menu()
        
        # Create main content
        self.create_main_content()
        
        # Create schedule display
        self.create_schedule_display()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import CSV", command=self.import_csv)
        file_menu.add_command(label="Save Schedule", command=self.save_schedule)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Employee menu
        employee_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Employee", menu=employee_menu)
        employee_menu.add_command(label="Add Employee", command=self.show_add_employee_dialog)

    def create_main_content(self):
        # Create buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add buttons
        ttk.Button(button_frame, text="Import CSV", command=self.import_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Employee", command=self.show_add_employee_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Generate Schedule", command=self.generate_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Schedule", command=self.save_schedule).pack(side=tk.LEFT, padx=5)

    def create_schedule_display(self):
        # Create schedule display frame
        self.schedule_frame = ttk.LabelFrame(self.main_frame, text="Weekly Schedule")
        self.schedule_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for schedule display
        self.schedule_tree = ttk.Treeview(self.schedule_frame, columns=("Monday", "Tuesday", "Wednesday", 
                                                                      "Thursday", "Friday", "Saturday", "Sunday"),
                                        show="headings")
        
        # Configure columns
        for day in self.scheduler.days:
            self.schedule_tree.heading(day, text=day)
            self.schedule_tree.column(day, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.schedule_frame, orient=tk.VERTICAL, command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def import_csv(self):
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            if self.scheduler.load_from_csv(filename):
                self.generate_schedule()
                messagebox.showinfo("Success", "Schedule imported successfully!")
            else:
                messagebox.showerror("Error", "Failed to import schedule. Please check the file format.")

    def show_add_employee_dialog(self):
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Employee")
        dialog.geometry("400x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        ttk.Label(dialog, text="Employee Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)
        
        # Create shift preference frames
        shift_frames = {}
        for day in self.scheduler.days:
            frame = ttk.LabelFrame(dialog, text=day)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            shift_var = tk.StringVar(value="N")
            for shift in [("Morning", "M"), ("Afternoon", "A"), ("Evening", "E"), ("No Shift", "N")]:
                ttk.Radiobutton(frame, text=shift[0], value=shift[1], 
                              variable=shift_var).pack(side=tk.LEFT, padx=5)
            shift_frames[day] = shift_var
        
        def save_employee():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter an employee name.")
                return
            
            preferred_shifts = {}
            for day, var in shift_frames.items():
                shift = Shift.from_code(var.get())
                if shift != Shift.NO_SHIFT:
                    preferred_shifts[day] = [shift]
            
            self.scheduler.add_employee(name, preferred_shifts)
            self.generate_schedule()
            dialog.destroy()
            messagebox.showinfo("Success", f"Employee {name} added successfully!")
        
        # Add save button
        ttk.Button(dialog, text="Save", command=save_employee).pack(pady=10)

    def generate_schedule(self):
        # Clear existing schedule
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        # Generate new schedule
        self.scheduler.generate_schedule()
        
        # Display schedule
        for shift in self.scheduler.shifts:
            row = [shift.value]
            for day in self.scheduler.days:
                employees = self.scheduler.schedule[day][shift]
                row.append(", ".join(employees) if employees else "No assignments")
            self.schedule_tree.insert("", tk.END, values=row)

    def save_schedule(self):
        filename = filedialog.asksaveasfilename(
            title="Save Schedule",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.scheduler.save_to_csv(filename)
            messagebox.showinfo("Success", f"Schedule saved to {filename}")

def main():
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 