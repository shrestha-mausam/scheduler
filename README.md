# Employee Schedule Manager

A scheduling application that manages employee shifts for a 7-day operation. The application allows employees to select their preferred shifts and ensures fair distribution of work while maintaining minimum coverage requirements.

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

1. Requirements:
   - C++17 compatible compiler (g++ or clang++)
   - Standard C++ library

2. Compile the application:
   ```bash
   g++ -std=c++17 scheduler.cpp -o scheduler
   ```
   or
   ```bash
   clang++ -std=c++17 scheduler.cpp -o scheduler
   ```
3. Run the application
    ```bash
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
# Example: test/all_shifts_assigned.csv

# C++ version
./scheduler
# When prompted, enter the path to the test file
# Example: test/all_shifts_assigned.csv
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

## Requirements

### Python Version
- Python 3.6 or higher
- Standard library modules: random, typing, dataclasses, enum, csv, os

### C++ Version
- C++17 or higher
- Standard library headers: iostream, vector, string, map, set, random, algorithm, memory, fstream, sstream, limits

## Notes

- The application ensures at least two employees per shift
- Employees cannot work more than one shift per day
- Employees cannot work more than five days per week
- The schedule is generated randomly when multiple valid options exist
- The application handles input validation and error cases
- Generated schedules can be saved to a new CSV file
- Test cases are provided to validate various scenarios and edge cases
