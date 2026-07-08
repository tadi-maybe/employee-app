import os
import sys
import time
import tkinter as tk
from tkinter import messagebox

# ENVIRONMENT & MODULE SETUP
# This ensures Python can locate and import custom modules from src.model and src.sortsearch.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(REPO_ROOT)

# Import domain model and other utility modules
from src.model.employee import Employee
from src.sortsearch.selection_sort import SelectionSort
from src.sortsearch.quick_sort import QuickSort
from src.sortsearch.binary_search import BinarySearch

# 2. FILE I/O UTILITY FUNCTIONS
def read_employee_file(file_path: str) -> list:
    """
    Reads employee data from a user-specified file path using the ◄► delimiter.
    Populates and returns a list of Employee objects. Uses explicit try-except-finally
    for safe resource management.
    """
    employees = []
    file_handle = None

    try:
        file_handle = open(file_path, 'r', encoding='utf-8')
        for line in file_handle:
            clean_line = line.strip()
            if not clean_line:
                continue
                
            # Parse record using the custom delimiter
            parts = clean_line.split("◄►")
            if len(parts) == 7:
                emp = Employee(
                    emp_id=int(parts[0]),
                    name=parts[1],
                    hours_worked=float(parts[2]),
                    hourly_rate=float(parts[3]),
                    deduction_prov=float(parts[4]),
                    deduction_fed=float(parts[5]),
                    education_allowance=float(parts[6])
                )
                employees.append(emp)
                
    except FileNotFoundError:
        print(f"[Error] File could not be found at path: {file_path}")
    except ValueError as val_err:
        print(f"[Error] Data parsing error: {val_err}")
    except Exception as exc:
        print(f"[Error] An unexpected error occurred while reading: {exc}")
    finally:
        # Guarantee resources are closed after use
        if file_handle:
            file_handle.close()
            
    return employees


def write_employee_csv(file_path: str, employees: list) -> None:
    """
    Exports a list of Employee objects out to standard CSV format.
    Format: ID,name,hoursWorked,hourlyRate,deductionProvince,deductionFederal,educationAllowance
    """
    file_handle = None
    try:
        file_handle = open(file_path, 'w', encoding='utf-8')
        for emp in employees:
            row = (
                f"{emp.emp_id},{emp.name},{emp.hours_worked},"
                f"{emp.hourly_rate},{emp.deduction_prov},"
                f"{emp.deduction_fed},{emp.education_allowance}\n"
            )
            file_handle.write(row)
    except Exception as exc:
        print(f"[Error] An error occurred while writing to {file_path}: {exc}")
    finally:
        if file_handle:
            file_handle.close()

# 3. MAIN EXECUTION CONTROLLER
def main():
    # Hide the main root Tkinter window so only the popup dialog appears
    root = tk.Tk()
    root.withdraw()

    # JOptionPane for OK Dialog Prompt
    messagebox.showinfo("Program Initiation", "Press OK to initiate the program!")

    
    # Prompt for Employee File Path
    file_path = input("Enter the full path of employee data file ◄► ").strip()
    
    # Clean surrounding quotation marks if copied directly from File Explorer
    file_path = file_path.strip('"').strip("'")

    salary_sorted_employees = read_employee_file(file_path)

    # Abort if data reading failed
    if not salary_sorted_employees:
        print(f"Could not read employee data from file {file_path}")
        return

    print(f"Read employee data from file {file_path}\n")

    # Create shallow copy for sorting by name
    name_sorted_employees = list(salary_sorted_employees)

    # Selection Sort (by Calculated Salary)
    for emp in salary_sorted_employees:
        emp.sort_key = 'salary'

    start_time_ms = time.time() * 1000
    SelectionSort.sort(salary_sorted_employees)
    selection_sort_duration = int((time.time() * 1000) - start_time_ms)

    # REQUIREMENT 4: QuickSort (by Name)
    for emp in name_sorted_employees:
        emp.sort_key = 'name'

    start_time_ms = time.time() * 1000
    QuickSort.sort(name_sorted_employees)
    quicksort_duration = int((time.time() * 1000) - start_time_ms)

    # REQUIREMENT 5: Print Timings in Exact Sample Format
    print("The performance of our sorting algorithms")
    print("###########################################")
    print(f"Selection Sort Time ► {selection_sort_duration} ms")
    print(f"Quick Sort Time ► {quicksort_duration} ms")
    print("###########################################\n\n")

    # Export Sorted Output CSV Files
    output_salary_path = os.path.join(REPO_ROOT, "sortedemployeeBySalary.csv")
    output_name_path = os.path.join(REPO_ROOT, "sortedemployeeByName.csv")

    write_employee_csv(output_salary_path, salary_sorted_employees)
    print(f"Write employee data sorted by their hourly salaries into file ◄► {output_salary_path}\n")

    write_employee_csv(output_name_path, name_sorted_employees)
    print(f"Write employee data sorted by their names into file ◄► {output_name_path}\n")

    # Interactive Recursive Binary Search Prompt
    search_name = input("Enter the name of the employee to search ◄► ").strip()

    if search_name:
        match_index = BinarySearch.search(name_sorted_employees, search_name)
        if match_index != -1:
            print(f"Employee found at index ◄► {match_index}")
        else:
            print(f"Employee found at index ◄► -1")


if __name__ == "__main__":
    main()
