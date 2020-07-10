# Employee-Attendance-Management-System
She Codes learning project for python course

## **Project Files**

#### **The project is built from 3 source files:**
1. **Main** - shows the navigation menu with all the options.
2. **Employees** - includes the Employee class and all related methods and functions.
3. **Attendances** - includes the Attendance class and all related functions.

#### **The data will be stored in 2 main files:**
1. **Employees.csv** - will include a header row and data about the employees
   _(ID, name, phone number and birthday)_.
2. **Attendance_log.csv** - will include a header row and the attendance data
   _(date, time, ID, name)_.

## **Project Functions**

#### The data structure:
1. **Employees:**  

    1.1. Uses Employee class with 4 fields: 
    - ID - 9 digits  
    - Name - a string, can include two words.  
    - Phone - 9/10 digits, can include a `-` after the prefix(2/3 first digits).  
    - Birthday - uses the template dd/mm/yyyy.   
    
    1.2. A dictionary is built based on the Employees.csv, using ID as key and Employee class instance as value.
2. **Attendance Log:** 
 
    2.1. Uses Attendance class with 4 fields: 
    - ID - 9 digits  
    - Name - a string, can include two or more words.
    - Date - uses the template dd/mm/yyyy (auto update on creation)
    - Time - uses the template HH:MM (auto update on creation)
    
    2.2. A list is built based on the Attendance_log.csv, using Attendance class instance as value.

#### Employees related functions: 
Each function updates employees file.  
1. Add employee manually - prompts the user for the data with template, includes verification and check for doubles based on ID.
2. Add employee from file - accepts a .csv file, adds the employees only if all the rows are valid. 
Prompts the user about the first encountered invalid row.
3. Delete employee manually - deletes an employee by ID, prompts if the employee doesn't exist or invalid ID.
4. Delete employees from file - accepts a .csv file, deletes the employees by ID only if all the supplied data is valid. 
Prompts the user with number of deleted users or first invalid row.

#### Attendance related functions:
5. Mark attendance - given an ID, creates a new Attendance record and updates attendance file.  
6. Generate attendance report of an employee - user enters ID and gets his attendance report(file). 
Prompts if the user doesn't exist or invalid or has no attendance registered.
7. Print an attendance report for a chosen month for all employees (active only) - prompts for month, 
will use current month as default and last year, generates a file.
8. Print an attendance report for all employees who were late (choose arrival time limit) - prompts for hour and start date, 
generates a report for all attendances after chosen hour from chosen date till now (file).
9. Print an attendance report by dates - prompts for dates and checks validity, creates a file.

#### More functions:
0. Exit the program - exits the program, prompts the user farewell.
