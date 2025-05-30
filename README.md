# Employee Schedule Manager

A scheduling application that manages employee shifts for a 7-day operation. The application allows employees to select their preferred shifts and generates a schedule that meets various requirements.

## Features

- Interactive command-line interface
- Import employee preferences from CSV file
- Manual entry of employee preferences
- Automatic schedule generation with conflict resolution
- Minimum coverage of two employees per shift
- Maximum of one shift per day per employee
- Maximum of five days per week per employee
- Export generated schedule to CSV file

## Input Format

The application accepts employee preferences in two ways:

1. CSV File Import:
   - File format: `employee_schedule.csv`
   - No header required
   - Each row represents one employee
   - Columns: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
   - Shift codes: M (Morning), A (Afternoon), E (Evening), N (No Shift)

2. Manual Entry:
   - Interactive prompts for employee name and shift preferences
   - Validates input for each day
   - Allows adding multiple employees

## Implementation

The application is implemented in both Python and C++.

### Python Implementation

```bash
# Run the Python version
python scheduler.py
```

### C++ Implementation

```bash
# Compile the C++ version
g++ -std=c++11 scheduler.cpp -o scheduler

# Run the C++ version
./scheduler
```

## Usage

1. Start the application
2. Choose from the menu:
   - Import schedule from CSV file
   - Enter employee preferences manually
   - Exit program
3. If importing from CSV:
   - Enter the filename (default: employee_schedule.csv)
4. If entering manually:
   - Enter employee name
   - For each day, enter shift preference (M/A/E/N)
   - Choose to add more employees or proceed
5. The application will generate and display the schedule
6. Option to save the generated schedule to a CSV file

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

## Requirements

### Python Version
- Python 3.6 or higher
- Standard library modules: random, typing, dataclasses, enum, csv, os

### C++ Version
- C++11 or higher
- Standard library headers: iostream, vector, string, map, set, random, algorithm, memory, fstream, sstream, limits

## Notes

- The application ensures at least two employees per shift
- Employees cannot work more than one shift per day
- Employees cannot work more than five days per week
- The schedule is generated randomly when multiple valid options exist
- The application handles input validation and error cases
- Generated schedules can be saved to a new CSV file
