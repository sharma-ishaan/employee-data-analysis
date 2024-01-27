# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import pandas as pd
from datetime import timedelta


def analyze_employee_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Convert time columns to datetime objects
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time Out'] = pd.to_datetime(df['Time Out'])

    # Handle the Timecard Hours (as Time) column with custom parsing
    df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'], errors='coerce')

    # Sort the DataFrame by employee name and time
    df.sort_values(['Employee Name', 'Time'], inplace=True)

    # Group data by employee name
    grouped_data = df.groupby('Employee Name')

    # Condition 1: People who have worked for 7 consecutive days
    for employee, group in grouped_data:
        consecutive_days = group['Time'].diff().dt.days == 1

        if consecutive_days.sum() >= 6:  # Check if there are at least 6 consecutive days (7 total)
            print(
                f"Employee Name: {employee}, Position: {group['Position ID'].iloc[0]}, worked for 7 consecutive days.")

    # Condition 2: People who have worked for more than 1 hour and less than 10 hours, including in between shifts
    for employee, group in grouped_data:
        # Sum up the total hours worked for each day
        total_hours_per_day = group.groupby(group['Time'].dt.date)[
                                  'Timecard Hours (as Time)'].sum().dt.total_seconds() / 3600

        # Check if any day satisfies the conditions
        if ((total_hours_per_day > 1) & (total_hours_per_day < 10)).any() or any(
                group['Time'].diff().dt.total_seconds().fillna(0) > 1 * 3600):
            print(
                f"Employee Name: {employee}, Position: {group['Position ID'].iloc[0]}, worked for more than 1 hour and less than 10 hours, including in between shifts.")

    # Condition 3: People who have worked continuously for more than 14 hours in a single shift
    for employee, group in grouped_data:
        more_than_14_hours = (group['Time Out'] - group['Time']).dt.total_seconds() / 3600 > 14

        if any(more_than_14_hours):
            print(
                f"Employee Name: {employee}, Position: {group['Position ID'].iloc[0]}, worked for more than 14 hours in a single shift.")


# Provide the file path as input
file_path = r'C:\Users\ISHAAN SHARMA\PycharmProjects\pythonProject1\Assignment_Timecard.xlsx - Sheet1.csv'  # Replace with the actual file path
analyze_employee_data(file_path)












