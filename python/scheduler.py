import random
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum
import csv
import os

class Shift(Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NO_SHIFT = "No Shift"

    @classmethod
    def from_code(cls, code: str) -> 'Shift':
        code_map = {
            'M': cls.MORNING,
            'A': cls.AFTERNOON,
            'E': cls.EVENING,
            'N': cls.NO_SHIFT
        }
        return code_map.get(code.upper(), cls.NO_SHIFT)

    @classmethod
    def to_code(cls, shift: 'Shift') -> str:
        code_map = {
            cls.MORNING: 'M',
            cls.AFTERNOON: 'A',
            cls.EVENING: 'E',
            cls.NO_SHIFT: 'N'
        }
        return code_map.get(shift, 'N')

@dataclass
class Employee:
    name: str
    preferred_shifts: Dict[str, List[Shift]]  # day -> list of preferred shifts
    assigned_shifts: Dict[str, Shift] = None  # day -> assigned shift
    days_worked: int = 0

    def __post_init__(self):
        if self.assigned_shifts is None:
            self.assigned_shifts = {}

class Scheduler:
    def __init__(self):
        self.employees: List[Employee] = []
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.shifts = [Shift.MORNING, Shift.AFTERNOON, Shift.EVENING]
        self.schedule: Dict[str, Dict[Shift, List[str]]] = {
            day: {shift: [] for shift in self.shifts} for day in self.days
        }

    def validate_csv_format(self, filename: str) -> tuple[bool, str]:
        """Validate the CSV file format before processing."""
        if not os.path.exists(filename):
            return False, f"Error: File {filename} does not exist."

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                
                # Check if file is empty
                if header is None:
                    return False, "Error: The input CSV file cannot be used because it is empty. Please provide a file with employee schedule data."

                # Validate header
                if len(header) != 8:
                    return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                f"First error encountered: Invalid header format.\n" \
                                f"Expected 8 columns (Name + 7 days of the week), but found {len(header)} columns.\n" \
                                f"Please ensure your CSV file has the following columns: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
                
                if header[0] != "Name":
                    return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                f"First error encountered: Invalid first column name.\n" \
                                f"Expected 'Name' as the first column, but found '{header[0]}'.\n" \
                                f"Please ensure your CSV file starts with a 'Name' column."
                
                # Validate day columns
                for i, day in enumerate(self.days, 1):
                    if i >= len(header) or header[i] != day:
                        return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                    f"First error encountered: Invalid column {i}.\n" \
                                    f"Expected '{day}', but found '{header[i] if i < len(header) else 'missing'}'.\n" \
                                    f"Please ensure your CSV file has the following columns in order: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."

                # Validate each row
                for row_num, row in enumerate(reader, 2):  # Start from 2 because we already read the header
                    if len(row) != 8:
                        return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                    f"First error encountered: Invalid number of columns in row {row_num}.\n" \
                                    f"Expected 8 columns, but found {len(row)} columns.\n" \
                                    f"Please ensure each row has values for Name and all 7 days of the week."
                    
                    # Check for empty name
                    if not row[0].strip():
                        return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                    f"First error encountered: Empty employee name in row {row_num}.\n" \
                                    f"Please ensure all employees have a name."
                    
                    # Validate shift codes
                    for i, shift_code in enumerate(row[1:], 1):
                        shift_code = shift_code.strip().upper()  # Trim whitespace and convert to uppercase
                        if shift_code not in ['M', 'A', 'E', 'N']:
                            return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                                        f"First error encountered: Invalid shift code in row {row_num}, column {i+1}.\n" \
                                        f"Found '{row[i]}', but only M (Morning), A (Afternoon), E (Evening), or N (No Shift) are allowed."

            return True, "CSV format is valid."

        except Exception as e:
            return False, f"Error: The input CSV file cannot be used because it does not follow the required format.\n" \
                         f"First error encountered: {str(e)}\n" \
                         f"Please ensure your file is a valid CSV file with the correct format."

    def load_from_csv(self, filename: str):
        """Load employee preferences from a CSV file."""
        # First validate the CSV format
        is_valid, error_message = self.validate_csv_format(filename)
        if not is_valid:
            print(error_message)
            return False

        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    name = row[0]
                    preferred_shifts = {}
                    
                    for i, shift_code in enumerate(row[1:], 1):
                        day = self.days[i-1]
                        shift = Shift.from_code(shift_code)
                        if shift != Shift.NO_SHIFT:
                            preferred_shifts[day] = [shift]
                    
                    self.add_employee(name, preferred_shifts)
            return True
        except Exception as e:
            print(f"Error processing CSV file: {str(e)}")
            return False

    def add_employee_manually(self):
        """Add an employee by manually entering their preferences."""
        name = input("\nEnter employee name: ").strip()
        if not name:
            print("Error: Name cannot be empty.")
            return False

        preferred_shifts = {}
        print("\nEnter shift preferences for each day (M=Morning, A=Afternoon, E=Evening, N=No Shift):")
        
        for day in self.days:
            while True:
                shift_code = input(f"{day} (M/A/E/N): ").strip().upper()
                if shift_code in ['M', 'A', 'E', 'N']:
                    shift = Shift.from_code(shift_code)
                    if shift != Shift.NO_SHIFT:
                        preferred_shifts[day] = [shift]
                    break
                else:
                    print("Invalid input. Please enter M, A, E, or N.")

        self.add_employee(name, preferred_shifts)
        return True

    def save_to_csv(self, filename: str):
        """Save current employee preferences to a CSV file."""
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Name'] + self.days)
            
            # Write employee data
            for emp in self.employees:
                row = [emp.name]
                for day in self.days:
                    if day in emp.preferred_shifts and emp.preferred_shifts[day]:
                        row.append(Shift.to_code(emp.preferred_shifts[day][0]))
                    else:
                        row.append('N')
                writer.writerow(row)

    def add_employee(self, name: str, preferred_shifts: Dict[str, List[Shift]]):
        """Add an employee with their preferred shifts."""
        employee = Employee(name=name, preferred_shifts=preferred_shifts)
        self.employees.append(employee)

    def get_available_employees(self, day: str, shift: Shift) -> List[Employee]:
        """Get employees who can work a specific shift on a given day."""
        return [
            emp for emp in self.employees
            if emp.days_worked < 5
            and day not in emp.assigned_shifts
            and shift in emp.preferred_shifts.get(day, [])
        ]

    def assign_shift(self, employee: Employee, day: str, shift: Shift):
        """Assign a shift to an employee."""
        employee.assigned_shifts[day] = shift
        employee.days_worked += 1
        self.schedule[day][shift].append(employee.name)

    def resolve_conflicts(self):
        """Resolve scheduling conflicts and ensure minimum coverage."""
        for day in self.days:
            for shift in self.shifts:
                # Get current assignments for this shift
                current_assignments = self.schedule[day][shift]
                
                # If we need more employees
                while len(current_assignments) < 2:
                    # Find available employees who haven't worked 5 days
                    available_employees = [
                        emp for emp in self.employees
                        if emp.days_worked < 5 and day not in emp.assigned_shifts
                    ]
                    
                    if not available_employees:
                        print(f"Warning: Cannot meet minimum coverage for {day} {shift.value}")
                        break
                    
                    # Randomly select an employee
                    employee = random.choice(available_employees)
                    self.assign_shift(employee, day, shift)
                    current_assignments = self.schedule[day][shift]

    def generate_schedule(self):
        """Generate the final schedule."""
        # First, try to assign preferred shifts
        for employee in self.employees:
            for day in self.days:
                if day in employee.preferred_shifts:
                    for preferred_shift in employee.preferred_shifts[day]:
                        if len(self.schedule[day][preferred_shift]) < 2:
                            self.assign_shift(employee, day, preferred_shift)
                            break

        # Resolve any conflicts and ensure minimum coverage
        self.resolve_conflicts()

    def print_schedule(self):
        """Print the final schedule in a readable format."""
        print("\nWeekly Schedule:")
        print("=" * 80)
        for day in self.days:
            print(f"\n{day}:")
            print("-" * 40)
            for shift in self.shifts:
                employees = self.schedule[day][shift]
                print(f"{shift.value}: {', '.join(employees) if employees else 'No assignments'}")

def main():
    scheduler = Scheduler()
    
    while True:
        print("\nEmployee Schedule Manager")
        print("1. Import schedule from CSV file")
        print("2. Enter employee preferences manually")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            filename = input("Enter CSV filename (default: employee_schedule.csv): ").strip()
            if not filename:
                filename = "../employee_schedule.csv"
            if scheduler.load_from_csv(filename):
                break
        elif choice == "2":
            while True:
                if scheduler.add_employee_manually():
                    add_more = input("\nAdd another employee? (y/n): ").strip().lower()
                    if add_more != 'y':
                        break
            break
        elif choice == "3":
            print("Exiting program.")
            return
        else:
            print("Invalid choice. Please try again.")

    # Generate and print the schedule
    scheduler.generate_schedule()
    scheduler.print_schedule()

    # Ask if user wants to save the schedule
    save_choice = input("\nDo you want to save the schedule to a CSV file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = input("Enter filename to save (default: employee_schedule.csv): ").strip()
        if not filename:
            filename = "employee_schedule.csv"
        scheduler.save_to_csv(filename)
        print(f"Schedule saved to {filename}")

if __name__ == "__main__":
    main() 