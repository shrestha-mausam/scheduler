import random
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum
import csv

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

    def load_from_csv(self, filename: str):
        """Load employee preferences from a CSV file."""
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) != 8:  # Name + 7 days
                    print(f"Warning: Invalid row format: {row}")
                    continue
                
                name = row[0]
                preferred_shifts = {}
                
                for i, shift_code in enumerate(row[1:], 1):
                    day = self.days[i-1]
                    shift = Shift.from_code(shift_code)
                    if shift != Shift.NO_SHIFT:
                        preferred_shifts[day] = [shift]
                
                self.add_employee(name, preferred_shifts)

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
    # Create a scheduler instance
    scheduler = Scheduler()
    
    # Load employee preferences from CSV file
    scheduler.load_from_csv('employee_schedule.csv')
    
    # Generate and print the schedule
    scheduler.generate_schedule()
    scheduler.print_schedule()

if __name__ == "__main__":
    main() 