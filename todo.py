# Import necessary libraries
from prettytable import PrettyTable, from_csv  # Import PrettyTable for tabular output
import csv  # Import CSV module for CSV file operations
import sys  # Import sys module for system-specific parameters and functions
from datetime import datetime, date  # Import datetime for date and time operations
import pandas as pd  # Import pandas for data manipulation and analysis


# Define fields for the CSV file
fields = ["Task_name", "Done?", "Created At", "Completed At"]
rows = []  # Initialize an empty list to store rows from the CSV file
filename = "todo.csv"  # Set the filename for the CSV file


def main():
    # Check if command-line arguments are provided
    if len(sys.argv) < 2:
        print("Welcome to Command-line Todo List")

    try:
        # Display help message if "-h" option is provided
        if sys.argv[1] == '-h':
            print("""
            1. Use -a <taskname> for adding a task.
            2. Use -d <taskname> for deleting a task.
            3. Use -c <taskname> for updating a task as completed.
            4. Use --show to see the to-do list.
            5. Use -csv to create a CSV file for storing user data.
            Note: Use -csv at the start. Using -csv will erase all user data.
            """)

        # Create a CSV file if "-csv" option is provided
        elif sys.argv[1] == '-csv':
            with open(filename, 'w') as writefile:
                csvwriter = csv.writer(writefile)
                csvwriter.writerow(fields)
                print("CSV file was created")

        # Add a task if "-a" option is provided
        elif sys.argv[1] == '-a':
            created_date_time = str(date.today()) + ' ' + datetime.now().strftime("%H:%M")
            taskname = sys.argv[2]
            task = [taskname, 'No', created_date_time, '!']
            addtaskcsv(task)

        # Display the to-do list if "--show" option is provided
        elif sys.argv[1] == '--show':
            ShowTable()

        # Delete a task if "-d" option is provided
        elif sys.argv[1] == '-d':
            name = sys.argv[2]
            deletefromcsv(name)

        # Update a task as completed if "-c" option is provided
        elif sys.argv[1] == '-c':
            taskname = sys.argv[2]
            updatecsv(taskname)

    except IndexError:
        print("You can use -h for help\n")
        sys.exit()


# Read existing tasks from the CSV file
with open(filename, 'r') as readfile:
    csvreader = csv.reader(readfile)
    for row in csvreader:
        rows.append(row)


# Function to display the to-do list
def ShowTable():
    try:
        with open("todo.csv") as fp:
            mytable = from_csv(fp)
        print(mytable)

    except:
        sys.exit("Empty CSV\nUse -csv to create a CSV file!\n")
    else:
        if len(rows) == 1:
            print('No tasks yet')


# Function to add a task to the CSV file
def addtaskcsv(task):
    df = pd.read_csv(filename)
    if task in df.Task_name.to_dict().values():
        sys.exit("Task already exists")
    else:
        with open(filename, 'a') as appendfile:
            csvappender = csv.writer(appendfile)
            csvappender.writerow(task)
            appendfile.close()
            print(f"{task[0]} was added to the table.")


# Function to delete a task from the CSV file
def deletefromcsv(taskname):
    if taskname == "Task_name":
        sys.exit("Invalid input")
    df = pd.read_csv(filename)
    if taskname in df.Task_name.to_dict().values():
        df = df.drop(df[df.Task_name == taskname].index)
        df.to_csv(filename, index=False)
        print(f"{taskname} was deleted!!!")
    else:
        print("Task doesn't exist")


# Function to update a task as completed in the CSV file
def updatecsv(taskname):
    df = pd.read_csv(filename)
    taskname_lst = list(df.Task_name.to_dict().values())
    try:
        num = taskname_lst.index(taskname)
    except ValueError:
        sys.exit("Task doesn't exist!")
    df.loc[num, 'Done?'] = 'Yes ✅'
    completed_at = str(date.today()) + ' ' + datetime.now().strftime("%H:%M")
    df.loc[num, 'Completed At'] = completed_at
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    main()
