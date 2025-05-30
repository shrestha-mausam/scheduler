# Employee Schedule Manager

This application manages employee schedules for a company that operates 7 days a week with morning, afternoon, and evening shifts.

## Features

- Input and storage of employee names and preferred shifts
- Automatic shift assignment with conflict resolution
- Ensures minimum coverage (2 employees per shift)
- Maximum 5 days per week per employee
- No more than one shift per day per employee
- Random assignment for unfilled shifts
- CSV file input support for employee preferences

## Input Format

The application reads employee preferences from a CSV file with the following format:

```
Name,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday
Employee1,N,N,M,A,E,N,N
Employee2,M,A,N,E,M,N,N
```

Where:
- First row is the header (will be skipped)
- Each subsequent row represents one employee
- Shift codes:
  - M = Morning Shift
  - A = Afternoon Shift
  - E = Evening Shift
  - N = No Shift (Not Available)

## Implementation

The application is implemented in both Python and C++:

### Python Version

To run the Python version:
```bash
python scheduler.py
```

### C++ Version

To compile and run the C++ version:
```bash
g++ -std=c++17 scheduler.cpp -o scheduler
./scheduler
```

## Usage

Both implementations provide the same functionality:

1. Create a CSV file named `employee_schedule.csv` with employee preferences
2. Place the CSV file in the same directory as the program
3. Run the program
4. The scheduler will:
   - Read employee preferences from the CSV file
   - Generate a schedule based on the preferences
   - Ensure minimum coverage (2 employees per shift)
   - Handle conflicts and random assignments when needed
   - Print the final schedule

## Example

The repository includes a sample `employee_schedule.csv` file with example data:

```
Name,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday
John,N,N,M,A,E,N,N
Alice,M,A,N,E,M,N,N
Bob,N,M,E,A,N,N,N
Carol,A,N,M,N,E,N,N
David,E,N,N,M,A,N,N
Emma,N,E,A,N,M,N,N
```

The scheduler will:
1. Read these preferences from the CSV file
2. Try to assign preferred shifts first
3. Ensure minimum coverage (2 employees per shift)
4. Resolve conflicts by randomly assigning available employees
5. Print the final schedule in a readable format

## Requirements

### Python Version
- Python 3.6 or higher
- No external dependencies required

### C++ Version
- C++17 compatible compiler
- Standard library support
