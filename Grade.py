import csv
import math
import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

# Init student counter along with overall total
i = 0
total = 0
# Create a list of class names and class totals to pick best performing class
class_name_list = []
class_average_list = []
proceed = True

# Would prompt user to enter file name.
averages = open('averages.csv', 'w', newline='')
fields = ['Class Name', 'Class Avg', 'Student Count', 'Student Count used in Avg', 'Excluded Students']
writer = csv.DictWriter(averages, fieldnames=fields)
writer.writeheader()

while proceed:
    root = tk.Tk()
    root.withdraw()

    # Prompt user to select file and extract file name from the path
    path = filedialog.askopenfilename()
    file_name = os.path.split(path)

    # Check to make sure file type is correct
    if file_name[1].endswith('.csv'):

        # Separate file name from extension
        class_name_list.append(str(Path(path).stem))

        # # Debug code
        # print('Added {}'.format(Path(path).stem))

        # Init individual class total
        class_total = 0
        with open(file_name[1], 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip title rows
            next(csv_reader)
            # Student used in avg count
            j = 0
            # Total student count
            k = 0
            # Init string to hold excluded student names
            excluded_students = '|'
            # Iterate through rows
            for line in csv_reader:

                # Remove student with 0 score and display student name
                try:
                    score = float(line[1])
                    if score == 0:
                        # # Debug code
                        # print('{} had a score of 0 and was ignored'.format(line[0]))
                        excluded_students += line[0] + '|'
                        k += 1

                    else:
                        # This is messy. May be able to use enumeration.
                        i += 1
                        j += 1
                        k += 1

                        # Add truncated student score to overall average
                        total += math.trunc(float(line[1]))

                        # Add truncated student score to class average
                        class_total += math.trunc(float(line[1]))

                except:
                    print('{} score of \'{}\' is invalid'.format(line[0], line[1]))

            # Try and find class average.
            try:
                c_avg = round(class_total / j, 1)
                class_average_list.append(c_avg)

                # # Debug to check lists
                # print(class_average_list)
                # print(class_name_list)
                writer.writerow({'Class Name': str(Path(path).stem), 'Class Avg': c_avg, 'Student Count': k,
                                 'Student Count used in Avg': j, 'Excluded Students': excluded_students})

            # If not possible pass, the error is displayed later.
            except:
                pass

    # If file selector dialogue box is cancelled or x'd out perform final calcs (probably use try catch)
    elif Path(path).stem == '':
        break

    # Alert user that the last file selected was invalid
    # Ignore the file but do not terminate selection process
    else:
        # # Debug code
        # print('({}) ignored due to invalid file type!'.format(Path(path).stem))
        writer.writerow({'Class Name': '({}) ignored due to invalid file type!'.format(Path(path).stem)})

avg = 0
try:
    total / i
    avg = total / i
    avg = round(avg, 1)
    # Enter an empty row for padding
    writer.writerow({'Class Name': ''})

    # # Debug code
    # print("{} = AVG of all students".format(avg))
    writer.writerow({'Class Name': "AVG of all students = {} ".format(avg)})

    max_avg = class_average_list.index(max(class_average_list))

    # # Debug code
    # print('{} has the highest class average at {}'.format(class_name_list[max_avg], class_average_list[max_avg]))
    writer.writerow({'Class Name': '{} has the highest class average at {}'.format(class_name_list[max_avg],
                                                                                   class_average_list[max_avg])})

except:
    # # Debug code
    # print("No classes selected or no valid student scores within selected classes")
    writer.writerow({'Class Name': 'No classes selected or no valid student scores within selected classes'})

# General Notes:
# The program only works when the csv is formatted correctly eg: Student Name in col 1 and grade in col 2
# Error checking for file type and grade validity is fairly robust. Could possibly give a warning for negative grades.
# Should allow for user to generate a name for the output file instead of overwriting the hardcoded one
# Would add a couple extra lines to give teachers an indication on if the test should be curved and provide
# a preferred curve score along with a max curve score.
