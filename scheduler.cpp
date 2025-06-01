#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <set>
#include <random>
#include <algorithm>
#include <memory>
#include <fstream>
#include <sstream>
#include <limits>

using namespace std;

enum class Shift {
    MORNING,
    AFTERNOON,
    EVENING,
    NO_SHIFT
};

// Convert shift code to Shift enum
Shift shiftFromCode(const string& code) {
    if (code == "M") return Shift::MORNING;
    if (code == "A") return Shift::AFTERNOON;
    if (code == "E") return Shift::EVENING;
    return Shift::NO_SHIFT;
}

// Convert Shift enum to shift code
string shiftToCode(Shift shift) {
    switch (shift) {
        case Shift::MORNING: return "M";
        case Shift::AFTERNOON: return "A";
        case Shift::EVENING: return "E";
        default: return "N";
    }
}

/**
 * Employee class represents a worker in the scheduling system.
 * It manages an employee's preferences, assigned shifts, and work constraints.
 * 
 * Key responsibilities:
 * - Stores employee's name and work history
 * - Tracks preferred shifts for each day
 * - Manages assigned shifts and days worked
 * - Enforces work constraints:
 *   * Maximum of 5 days per week
 *   * One shift per day maximum
 *   * Only assigned to preferred shifts
 * 
 * The class is used by the Scheduler to:
 * - Validate shift assignments
 * - Track employee availability
 * - Maintain work hour limits
 * - Store shift preferences
 */
class Employee {
public:
    Employee(const string& name) : name(name), days_worked(0) {}

    void addPreferredShift(const string& day, Shift shift) {
        if (shift != Shift::NO_SHIFT) {
            preferred_shifts[day].push_back(shift);
        }
    }

    bool canWork(const string& day, Shift shift) const {
        auto it = preferred_shifts.find(day);
        if (it == preferred_shifts.end()) {
            return false;
        }
        return days_worked < 5 && 
               assigned_shifts.find(day) == assigned_shifts.end() &&
               find(it->second.begin(), it->second.end(), shift) != it->second.end();
    }

    void assignShift(const string& day, Shift shift) {
        assigned_shifts[day] = shift;
        days_worked++;
    }

    string getName() const { return name; }
    int getDaysWorked() const { return days_worked; }
    bool isAssigned(const string& day) const {
        return assigned_shifts.find(day) != assigned_shifts.end();
    }

private:
    string name;
    map<string, vector<Shift>> preferred_shifts;
    map<string, Shift> assigned_shifts;
    int days_worked;
};

/**
 * The Scheduler class is responsible for managing employee schedules in a 7-day operation.
 * It handles the creation, validation, and management of work schedules while ensuring
 * fair distribution of shifts and maintaining minimum coverage requirements.
 * 
 * Key responsibilities:
 * - Loading employee preferences from CSV files
 * - Manual entry of employee preferences
 * - Generating valid schedules that meet all constraints
 * - Validating schedule requirements:
 *   * Minimum of 2 employees per shift
 *   * Maximum of 1 shift per day per employee
 *   * Maximum of 5 days per week per employee
 * - Saving generated schedules to CSV files
 * - Displaying schedules in a readable format
 * 
 * The class maintains internal state including:
 * - List of valid days (Monday through Sunday)
 * - List of valid shifts (Morning, Afternoon, Evening)
 * - Collection of employee objects with their preferences
 * - Current schedule mapping days and shifts to assigned employees
 */
class Scheduler {
public:
    Scheduler() {
        days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
        shifts = {Shift::MORNING, Shift::AFTERNOON, Shift::EVENING};
        
        // Initialize schedule
        for (const auto& day : days) {
            for (const auto& shift : shifts) {
                schedule[day][shift] = vector<string>();
            }
        }
    }

    pair<bool, string> validateCSVFormat(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            return {false, "Error: The input CSV file cannot be used because it does not exist.\n"
                          "Please ensure the file exists and you have permission to read it."};
        }

        string line;
        // Read header
        if (!getline(file, line)) {
            return {false, "Error: The input CSV file cannot be used because it is empty.\n"
                          "Please provide a file with employee schedule data."};
        }

        stringstream ss(line);
        string token;
        vector<string> header;

        while (getline(ss, token, ',')) {
            // Trim whitespace from header
            token.erase(0, token.find_first_not_of(" \t\r\n"));
            token.erase(token.find_last_not_of(" \t\r\n") + 1);
            header.push_back(token);
        }

        // Validate header
        if (header.size() != 8) {
            return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                          "First error encountered: Invalid header format.\n"
                          "Expected 8 columns (Name + 7 days of the week), but found " + to_string(header.size()) + " columns.\n"
                          "Please ensure your CSV file has the following columns: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."};
        }

        if (header[0] != "Name") {
            return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                          "First error encountered: Invalid first column name.\n"
                          "Expected 'Name' as the first column, but found '" + header[0] + "'.\n"
                          "Please ensure your CSV file starts with a 'Name' column."};
        }

        // Validate day columns
        for (size_t i = 0; i < days.size(); ++i) {
            if (i + 1 >= header.size() || header[i + 1] != days[i]) {
                return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                              "First error encountered: Invalid column " + to_string(i + 1) + ".\n"
                              "Expected '" + days[i] + "', but found '" + (i + 1 < header.size() ? header[i + 1] : "missing") + "'.\n"
                              "Please ensure your CSV file has the following columns in order: Name, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."};
            }
        }

        // Validate each row
        int row_num = 2;  // Start from 2 because we already read the header
        while (getline(file, line)) {
            stringstream row_ss(line);
            vector<string> row;
            
            while (getline(row_ss, token, ',')) {
                // Trim whitespace from each token
                token.erase(0, token.find_first_not_of(" \t\r\n"));
                token.erase(token.find_last_not_of(" \t\r\n") + 1);
                row.push_back(token);
            }

            if (row.size() != 8) {
                return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                              "First error encountered: Invalid number of columns in row " + to_string(row_num) + ".\n"
                              "Expected 8 columns, but found " + to_string(row.size()) + " columns.\n"
                              "Please ensure each row has values for Name and all 7 days of the week."};
            }

            // Check for empty name
            if (row[0].empty()) {
                return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                              "First error encountered: Empty employee name in row " + to_string(row_num) + ".\n"
                              "Please ensure all employees have a name."};
            }

            // Validate shift codes
            for (size_t i = 1; i < row.size(); ++i) {
                string code = row[i];
                transform(code.begin(), code.end(), code.begin(), ::toupper);
                if (code != "M" && code != "A" && code != "E" && code != "N") {
                    return {false, "Error: The input CSV file cannot be used because it does not follow the required format.\n"
                                  "First error encountered: Invalid shift code in row " + to_string(row_num) + 
                                  ", column " + to_string(i + 1) + ".\n"
                                  "Found '" + row[i] + "', but only M (Morning), A (Afternoon), E (Evening), or N (No Shift) are allowed."};
                }
            }
            row_num++;
        }

        return {true, "CSV format is valid."};
    }

    bool loadFromCSV(const string& filename) {
        // First validate the CSV format
        auto [is_valid, error_message] = validateCSVFormat(filename);
        if (!is_valid) {
            cerr << error_message << endl;
            return false;
        }

        try {
            ifstream file(filename);
            string line;
            // Skip header
            getline(file, line);

            while (getline(file, line)) {
                stringstream ss(line);
                string token;
                vector<string> row;

                while (getline(ss, token, ',')) {
                    row.push_back(token);
                }

                string name = row[0];
                addEmployee(name);

                for (size_t i = 1; i < row.size(); ++i) {
                    string day = days[i-1];
                    Shift shift = shiftFromCode(row[i]);
                    addPreferredShift(name, day, shift);
                }
            }

            return true;
        } catch (const exception& e) {
            cerr << "Error processing CSV file: " << e.what() << endl;
            return false;
        }
    }

    bool addEmployeeManually() {
        string name;
        cout << "\nEnter employee name: ";
        getline(cin, name);
        
        if (name.empty()) {
            cout << "Error: Name cannot be empty." << endl;
            return false;
        }

        addEmployee(name);

        cout << "\nEnter shift preferences for each day (M=Morning, A=Afternoon, E=Evening, N=No Shift):" << endl;
        
        for (const auto& day : days) {
            while (true) {
                string shift_code;
                cout << day << " (M/A/E/N): ";
                getline(cin, shift_code);
                
                // Convert to uppercase
                transform(shift_code.begin(), shift_code.end(), shift_code.begin(), ::toupper);
                
                if (shift_code == "M" || shift_code == "A" || shift_code == "E" || shift_code == "N") {
                    Shift shift = shiftFromCode(shift_code);
                    addPreferredShift(name, day, shift);
                    break;
                } else {
                    cout << "Invalid input. Please enter M, A, E, or N." << endl;
                }
            }
        }

        return true;
    }

    void saveToCSV(const string& filename) {
        ofstream file(filename);
        if (!file.is_open()) {
            cerr << "Error: Could not open file " << filename << " for writing." << endl;
            return;
        }

        // Write header
        file << "Name";
        for (const auto& day : days) {
            file << "," << day;
        }
        file << endl;

        // Write employee data
        for (const auto& emp : employees) {
            file << emp->getName();
            for (const auto& day : days) {
                file << ",";
                if (emp->canWork(day, Shift::MORNING)) {
                    file << "M";
                } else if (emp->canWork(day, Shift::AFTERNOON)) {
                    file << "A";
                } else if (emp->canWork(day, Shift::EVENING)) {
                    file << "E";
                } else {
                    file << "N";
                }
            }
            file << endl;
        }
    }

    void addEmployee(const string& name) {
        employees.push_back(make_unique<Employee>(name));
    }

    void addPreferredShift(const string& employee_name, const string& day, Shift shift) {
        for (const auto& emp : employees) {
            if (emp->getName() == employee_name) {
                emp->addPreferredShift(day, shift);
                break;
            }
        }
    }

    vector<Employee*> getAvailableEmployees(const string& day, Shift shift) {
        vector<Employee*> available;
        for (const auto& emp : employees) {
            if (emp->canWork(day, shift)) {
                available.push_back(emp.get());
            }
        }
        return available;
    }

    void assignShift(Employee* employee, const string& day, Shift shift) {
        employee->assignShift(day, shift);
        schedule[day][shift].push_back(employee->getName());
    }

    void resolveConflicts() {
        for (const auto& day : days) {
            for (const auto& shift : shifts) {
                auto& current_assignments = schedule[day][shift];
                
                while (current_assignments.size() < 2) {
                    vector<Employee*> available_employees;
                    for (const auto& emp : employees) {
                        if (emp->getDaysWorked() < 5 && !emp->isAssigned(day)) {
                            available_employees.push_back(emp.get());
                        }
                    }

                    if (available_employees.empty()) {
                        cout << "Warning: Cannot meet minimum coverage for " << day << " ";
                        switch (shift) {
                            case Shift::MORNING: cout << "Morning"; break;
                            case Shift::AFTERNOON: cout << "Afternoon"; break;
                            case Shift::EVENING: cout << "Evening"; break;
                            default: break;
                        }
                        cout << endl;
                        break;
                    }

                    // Random selection
                    random_device rd;
                    mt19937 gen(rd());
                    uniform_int_distribution<> dis(0, available_employees.size() - 1);
                    Employee* selected = available_employees[dis(gen)];
                    assignShift(selected, day, shift);
                }
            }
        }
    }

    void generateSchedule() {
        // First, try to assign preferred shifts
        for (const auto& emp : employees) {
            for (const auto& day : days) {
                // Check all shifts for the day, starting with preferred shifts
                if (emp->canWork(day, Shift::MORNING) && schedule[day][Shift::MORNING].size() < 2) {
                    assignShift(emp.get(), day, Shift::MORNING);
                }
                if (emp->canWork(day, Shift::AFTERNOON) && schedule[day][Shift::AFTERNOON].size() < 2) {
                    assignShift(emp.get(), day, Shift::AFTERNOON);
                }
                if (emp->canWork(day, Shift::EVENING) && schedule[day][Shift::EVENING].size() < 2) {
                    assignShift(emp.get(), day, Shift::EVENING);
                }
            }
        }

        // Resolve conflicts and ensure minimum coverage
        resolveConflicts();
    }

    void printSchedule() const {
        cout << "\nWeekly Schedule:" << endl;
        cout << string(80, '=') << endl;

        for (const auto& day : days) {
            cout << "\n" << day << ":" << endl;
            cout << string(40, '-') << endl;

            for (const auto& shift : shifts) {
                string shift_name;
                switch (shift) {
                    case Shift::MORNING: shift_name = "Morning"; break;
                    case Shift::AFTERNOON: shift_name = "Afternoon"; break;
                    case Shift::EVENING: shift_name = "Evening"; break;
                    default: continue;
                }
                
                cout << shift_name << ": ";
                
                // Safely access the schedule map
                auto day_it = schedule.find(day);
                if (day_it != schedule.end()) {
                    auto shift_it = day_it->second.find(shift);
                    if (shift_it != day_it->second.end()) {
                        const auto& employees = shift_it->second;
                        if (employees.empty()) {
                            cout << "No assignments";
                        } else {
                            for (size_t i = 0; i < employees.size(); ++i) {
                                cout << employees[i];
                                if (i < employees.size() - 1) cout << ", ";
                            }
                        }
                    } else {
                        cout << "No assignments";
                    }
                } else {
                    cout << "No assignments";
                }
                cout << endl;
            }
        }
    }

private:
    vector<string> days;
    vector<Shift> shifts;
    vector<unique_ptr<Employee>> employees;
    map<string, map<Shift, vector<string>>> schedule;
};

/**
 * Clears the input buffer to prevent any leftover input from affecting subsequent reads.
 * This is particularly useful after numeric input operations where newline characters
 * might remain in the buffer and cause unexpected behavior in subsequent getline() calls.
 * The method clears any error flags and discards all characters up to the next newline.
 */
void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

int main() {
    Scheduler scheduler;
    
    while (true) {
        cout << "\nEmployee Schedule Manager" << endl;
        cout << "1. Import schedule from CSV file" << endl;
        cout << "2. Enter employee preferences manually" << endl;
        cout << "3. Exit" << endl;
        
        cout << "\nEnter your choice (1-3): ";
        string choice;
        getline(cin, choice);
        
        if (choice == "1") {
            cout << "Enter CSV filename (default: employee_schedule.csv): ";
            string filename;
            getline(cin, filename);
            if (filename.empty()) {
                filename = "employee_schedule.csv";
            }
            if (scheduler.loadFromCSV(filename)) {
                break;
            }
        } else if (choice == "2") {
            while (true) {
                if (scheduler.addEmployeeManually()) {
                    cout << "\nAdd another employee? (y/n): ";
                    string add_more;
                    getline(cin, add_more);
                    if (add_more != "y" && add_more != "Y") {
                        break;
                    }
                }
            }
            break;
        } else if (choice == "3") {
            cout << "Exiting program." << endl;
            return 0;
        } else {
            cout << "Invalid choice. Please try again." << endl;
        }
    }

    // Generate and print the schedule
    scheduler.generateSchedule();
    scheduler.printSchedule();

    // Ask if user wants to save the schedule
    cout << "\nDo you want to save the schedule to a CSV file? (y/n): ";
    string save_choice;
    getline(cin, save_choice);
    if (save_choice == "y" || save_choice == "Y") {
        cout << "Enter filename to save (default: employee_schedule.csv): ";
        string filename;
        getline(cin, filename);
        if (filename.empty()) {
            filename = "employee_schedule.csv";
        }
        scheduler.saveToCSV(filename);
        cout << "Schedule saved to " << filename << endl;
    }

    return 0;
} 