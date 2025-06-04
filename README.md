# Employee Schedule Manager

A scheduling application that manages employee shifts for a 7-day operation. The application allows employees to select their preferred shifts and ensures fair distribution of work while maintaining minimum coverage requirements.

## Features

- Interactive GUI interface (Python) and command-line interface (C++)
- Import employee preferences from CSV file
- Manual entry of employee preferences
- Automatic schedule generation with conflict resolution
- Minimum coverage of two employees per shift
- Maximum of one shift per day per employee
- Maximum of five days per week per employee
- Export generated schedule to CSV file

## Project Structure
```
scheduler/
├── python/              # Python implementation
│   ├── scheduler.py     # Core scheduling logic
│   ├── scheduler_gui.py # GUI implementation
│   └── requirements.txt # Python dependencies
├── cpp/                 # C++ implementation
│   └── scheduler.cpp    # C++ implementation
├── test/               # Test files
│   └── *.csv           # Test CSV files
└── README.md           # This file
```

## Python Implementation

### Requirements
- Python 3.8 or higher
- Tkinter (GUI library, comes with Python)

### Installation

1. Navigate to the Python implementation directory:
```bash
cd python
```

2. Create a virtual environment (recommended):
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

2. Manual Entry:
   - Interactive prompts for employee name and shift preferences
   - Validates input for each day
   - Allows adding multiple employees

## Implementation

### Running the Python Application

1. Start the GUI application:
```bash
python scheduler_gui.py
```

2. Or run the command-line version:
```bash
python scheduler.py
```

## C++ Implementation

### Requirements
- C++17 compatible compiler (g++ or clang++)
- Standard C++ library

### Compilation

1. Navigate to the C++ implementation directory:
```bash
cd cpp
```

2. Compile the application:
```bash
# Using g++
g++ -std=c++17 scheduler.cpp -o scheduler

# Using clang++
clang++ -std=c++17 scheduler.cpp -o scheduler
```

### Running the C++ Application

1. Run the compiled executable:
```bash
# On macOS/Linux
./scheduler

# On Windows
scheduler.exe
```

## Usage

### Python GUI Version
1. Start the application using `python scheduler_gui.py`
2. Use the menu or buttons to:
   - Import schedule from CSV file
   - Add employee preferences manually
   - Generate schedule
   - Save schedule to CSV file

### Python Command-line Version
1. Start the application using `python scheduler.py`
2. Follow the interactive prompts to:
   - Import schedule from CSV file
   - Enter employee preferences manually
   - Generate and save schedule

### C++ Version
1. Start the application using `./scheduler`
2. Follow the interactive prompts to:
   - Import schedule from CSV file
   - Enter employee preferences manually
   - Generate and save schedule

## Input Format

The application accepts employee preferences in two ways:

1. CSV File Import:
   - File format: `employee_schedule.csv`
   - Header required: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
   - Each row represents one employee
   - Shift codes: M (Morning), A (Afternoon), E (Evening), N (No Shift)

2. Manual Entry:
   - Interactive prompts for employee name and shift preferences
   - Validates input for each day
   - Allows adding multiple employees

## Test Cases

The `test` directory contains various test CSV files to validate the scheduler's functionality:

1. `all_shifts_assigned.csv`
   - All shifts are assigned with more than 2 employees per shift
   - Tests maximum capacity handling

2. `some_shifts_unassigned.csv`
   - Some shifts are not assigned
   - Tests conflict resolution and random assignment

3. `invalid_format.csv`
   - Contains missing columns and invalid rows
   - Tests error handling for malformed input

4. `invalid_shift_codes.csv`
   - Contains invalid shift codes (X, Y, Z)
   - Tests input validation

5. `empty_names.csv`
   - Contains rows with empty employee names
   - Tests name validation

6. `max_work_days.csv`
   - Employees assigned to 6 days
   - Tests the 5-day maximum constraint

7. `minimum_coverage.csv`
   - Each shift has exactly 2 employees
   - Tests minimum coverage requirement

To run tests:
```bash
# Python version
python scheduler.py
# When prompted, enter the path to the test file
# Example: ../test/all_shifts_assigned.csv

# C++ version
./scheduler
# When prompted, enter the path to the test file
# Example: ../test/all_shifts_assigned.csv
```

## Example CSV File

```
Name,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday
John,N,N,M,A,E,N,N
Alice,M,A,N,E,M,N,N
Bob,N,M,E,A,N,N,N
Carol,A,N,M,N,E,N,N
David,E,N,N,M,A,N,N
Emma,N,E,A,N,M,N,N
```

## Notes

- The application ensures at least two employees per shift
- Employees cannot work more than one shift per day
- Employees cannot work more than five days per week
- The schedule is generated randomly when multiple valid options exist
- The application handles input validation and error cases
- Generated schedules can be saved to a new CSV file
- Test cases are provided to validate various scenarios and edge cases
