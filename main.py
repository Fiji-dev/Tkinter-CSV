import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import os
import datetime

# CSV file for storing data
CSV_FILE = "marks_data.csv"

# Ensure the CSV file exists and has a header
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Student ID", "Student Name", "Module Code", "Module Name",
                "Coursework Mark 1", "Coursework Mark 2", "Coursework Mark 3",
                "Gender", "Date of Entry", "Total Marks",
            ])

# Read all data from the CSV
def read_csv():
    try:
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            data = [row for row in reader if any(cell.strip() for cell in row)]  # Remove empty rows
            return data
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file: {str(e)}")
        return []


# Write data to the CSV
def write_csv(rows):
    try:
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    except Exception as e:
        messagebox.showerror("Error", f"Could not write to file: {str(e)}")


# Append a single row to the CSV
def append_to_csv(row):
    try:
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save data: {str(e)}")


# Clear the frame for new page content
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

def home_page():
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def get_statistics(data):
        if len(data) <= 1:
            return 0, 0  # No students or modules if only the header is present

        # Exclude the header row
        number_of_students = len(data) - 1
        module_codes = [row[2] for row in data[1:] if row[2].strip()]
        unique_modules = len(set(module_codes))

        return number_of_students, unique_modules

    # Clear existing content
    clear_frame()

    # Constants
    FONT_STYLE = ("Helvetica", 14)
    HEADER_FONT_STYLE = ("Helvetica", 20)
    BACKGROUND_COLOR = "#B3E5FC"

    # Welcome Label
    tk.Label(frame, text="Welcome to the Mark Registration System", font=HEADER_FONT_STYLE, bg=BACKGROUND_COLOR).pack(
        pady=20)

    # Reading CSV data
    data = read_csv()
    number_of_students, module_codes = get_statistics(data)

    # Displaying statistics
    number_of_students, unique_modules = get_statistics(data)

    tk.Label(frame, text=f"Number of Students: {number_of_students}", font=FONT_STYLE, bg=BACKGROUND_COLOR).pack(
        pady=10)
    tk.Label(frame, text=f"Number of Modules: {unique_modules}", font=FONT_STYLE, bg=BACKGROUND_COLOR).pack(pady=10)


def input_marks_page():
    clear_frame()
    frame.pack_propagate(False)  # Prevent resizing

    # Title (centered with reduced padding)
    tk.Label(frame, text="Input Marks", font=("Helvetica", 16), bg="#B3E5FC").place(relx=0.5, rely=0.1, anchor="center")

    # Sub-frame for centering content
    content_frame = tk.Frame(frame, bg="#B3E5FC")
    content_frame.place(relx=0.5, rely=0.4, anchor="center")  # Center the content

    # Fields for input
    fields = [
        "Student ID", "Student Name", "Module Code", "Module Name", "Coursework Mark 1",
        "Coursework Mark 2", "Coursework Mark 3", "Gender", "Date of Entry"
    ]
    entries = []

    for idx, field in enumerate(fields):
        tk.Label(content_frame, text=field, font=("Helvetica", 12), bg="#B3E5FC", anchor="e", width=20).grid(row=idx,
                                                                                                             column=0,
                                                                                                             padx=10,
                                                                                                             pady=5)

        if field == "Gender":
            gender_combobox = ttk.Combobox(content_frame, font=("Helvetica", 12), values=["Male", "Female"])
            gender_combobox.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            gender_combobox.set("")  # Default selection
            entries.append(gender_combobox)
        else:
            entry = tk.Entry(content_frame, font=("Helvetica", 12))
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="we")
            entries.append(entry)

    # Validate marks
    def validate_marks(entries):
        try:
            marks = [int(entry.get().strip()) for entry in entries[4:7]]  # Coursework Marks
            return all(0 <= mark <= 100 for mark in marks)
        except ValueError:
            return False

    # Function to submit marks
    def submit_marks():
        if not validate_inputs(entries):
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        if not validate_marks(entries):
            messagebox.showerror("Validation Error", "Marks must be numeric and between 0 and 100!")
            return

        data = [entry.get().strip() for entry in entries]

        # Calculate the total marks
        coursework_marks = [int(data[4]), int(data[5]), int(data[6])]
        total_marks = sum(coursework_marks)
        data.append(str(total_marks))  # Append the total marks

        append_to_csv(data)  # Save to CSV file
        messagebox.showinfo("Success", "Marks submitted successfully!")
        reset_inputs(entries)
        entries[0].config(state="normal")  # Make Student ID editable for regeneration
        entries[0].delete(0, tk.END)
        entries[0].config(state="readonly")

        # Buttons side by side

    button_frame = tk.Frame(content_frame, bg="#B3E5FC")
    button_frame.grid(row=len(fields), columnspan=2, pady=10)

    tk.Button(button_frame, text="Submit", command=submit_marks, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(
        side="left", padx=10)
    tk.Button(button_frame, text="Reset", command=lambda: reset_inputs(entries), font=("Helvetica", 12), bg="#F44336",
              fg="white").pack(side="left", padx=10)


def validate_inputs(entries):
    return all(entry.get().strip() for entry in entries)


def reset_inputs(inputs):
    for input_field in inputs:
        if isinstance(input_field, tk.Entry):
            input_field.delete(0, tk.END)
        elif isinstance(input_field, ttk.Combobox):
            input_field.set("")

# Update marks page
def update_marks_page():
    clear_frame()
    frame.pack_propagate(False)  # Prevent resizing

    # Title
    tk.Label(frame, text="Update Marks", font=("Helvetica", 16), bg="#B3E5FC").pack(pady=80)

    # Sub-frame for centering content
    content_frame = tk.Frame(frame, bg="#B3E5FC")
    content_frame.place(relx=0.5, rely=0.4, anchor="center")  # Center the content slightly lower

    # Fields for updating marks
    fields = [
        "Student ID", "Module Code", "Coursework Mark 1",
        "Coursework Mark 2", "Coursework Mark 3", "Date of Entry"
    ]
    entries = []

    for idx, field in enumerate(fields):
        tk.Label(content_frame, text=field, font=("Helvetica", 12), bg="#B3E5FC", anchor="e", width=20).grid(
            row=idx, column=0, padx=5, pady=5, sticky="e"
        )
        entry = tk.Entry(content_frame, font=("Helvetica", 12))
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="we")
        entries.append(entry)

    # Function to validate marks
    def validate_marks(entries):
        try:
            marks = [int(entry.get().strip()) for entry in entries[2:5]]
            return all(0 <= mark <= 100 for mark in marks)
        except ValueError:
            return False

    # Function to update marks
    def update_marks():
        if not validate_inputs(entries):
            messagebox.showerror("Validation Error", "All fields are required!")
            return

        if not validate_marks(entries):
            messagebox.showerror("Validation Error", "Marks must be numeric and between 0 and 100!")
            return

        student_id, module_code, mark1, mark2, mark3, date = [entry.get().strip() for entry in entries]
        data = read_csv()
        updated = False

        for row in data:
            if row[0] == student_id and row[2] == module_code:
                row[4], row[5], row[6] = mark1, mark2, mark3
                updated = True

        if updated:
            write_csv(data)
            messagebox.showinfo("Success", "Marks updated successfully!")
            reset_inputs(entries)
        else:
            messagebox.showerror("Error", "Record not found!")

    # Buttons side by side using grid instead of pack
    button_frame = tk.Frame(content_frame, bg="#B3E5FC")
    button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="Update", command=update_marks, font=("Helvetica", 12), bg="#FF9800", fg="white").grid(
        row=0, column=0, padx=5
    )
    tk.Button(button_frame, text="Reset", command=lambda: reset_inputs(entries), font=("Helvetica", 12),
              bg="#F44336", fg="white").grid(row=0, column=1, padx=5)


# View marks page
def view_marks_page():
    clear_frame()
    frame.pack_propagate(False)  # Prevent resizing

    # Title (centered)
    tk.Label(frame, text="View Marks", font=("Helvetica", 16, "bold"), bg="#B3E5FC").place(relx=0.5, rely=0.05,
                                                                                           anchor="center")

    # Module Code Input Section
    input_frame = tk.Frame(frame, bg="#B3E5FC")
    input_frame.place(relx=0.5, rely=0.15, anchor="center")

    tk.Label(input_frame, text="Module Code:", font=("Helvetica", 12), bg="#B3E5FC", anchor="e", width=15).grid(row=0,
                                                                                                                column=0,
                                                                                                                padx=10,
                                                                                                                pady=5)
    module_code_entry = tk.Entry(input_frame, font=("Helvetica", 12), width=20)
    module_code_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

    # Buttons Section
    button_frame = tk.Frame(frame, bg="#B3E5FC")
    button_frame.place(relx=0.5, rely=0.25, anchor="center")

    tk.Button(button_frame, text="View", command=lambda: view_marks(module_code_entry.get()), font=("Helvetica", 12),
              bg="#FFC107", fg="black", width=10).pack(side="left", padx=5)
    tk.Button(button_frame, text="Clear", command=lambda: clear_page(module_code_entry), font=("Helvetica", 12),
              bg="#F44336", fg="white", width=10).pack(side="left", padx=5)

    # Table Section
    table_frame = tk.Frame(frame, bg="#B3E5FC")
    table_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.4)

    def view_marks(module_code):
        module_code = module_code.strip().upper()
        if not module_code:
            messagebox.showerror("Validation Error", "Module code is required!")
            return

        for widget in table_frame.winfo_children():
            widget.destroy()

        data = read_csv()
        filtered_data = [row for row in data if row[2].upper() == module_code]

        if filtered_data:
            columns = (
                "Student ID", "Student Name", "Module Code", "Module Name", "Coursework Mark 1", "Coursework Mark 2",
                "Coursework Mark 3", "Gender", "Date of Entry")
            tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)

            for col in columns:
                tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
                tree.column(col, width=100, anchor="center")

            for row in filtered_data:
                tree.insert("", "end", values=row)

            tree.pack(side="left", fill="both", expand=True)

            # Improved Scrollbar Placement
            scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            scrollbar_y.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
            tree.configure(yscrollcommand=scrollbar_y.set)

            scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
            scrollbar_x.place(relx=0, rely=1.0, relwidth=1.0, anchor='sw')
            tree.configure(xscrollcommand=scrollbar_x.set)
        else:
            messagebox.showinfo("No Records", f"No records found for module {module_code}.")

    def sort_column(tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=reverse)
        for idx, item in enumerate(data):
            tree.move(item[1], "", idx)
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    def clear_page(entry):
        entry.delete(0, tk.END)
        for widget in table_frame.winfo_children():
            widget.destroy()

# Visualization page
def visualize_page():
    clear_frame()
    tk.Label(frame, text="Visualization", font=("Helvetica", 16), bg="#B3E5FC").pack(pady=10)

    def show_horizontal_bar_chart():
        data = read_csv()
        if not data:
            return

        try:
            # Create a dictionary to count students for each module
            module_counts = {}
            for row in data[1:]:  # Skip the header row
                if len(row) < 3:  # Skip invalid rows
                    continue
                module = row[2]  # Assuming module names are in the 3rd column
                module_counts[module] = module_counts.get(module, 0) + 1

            if not module_counts:
                messagebox.showerror("Error", "No valid module data found in the CSV.")
                return

            # Extract modules (categories) and their counts (values)
            categories = list(module_counts.keys())
            values = list(module_counts.values())

            plt.figure(figsize=(10, 6))
            plt.barh(categories, values, color="#64B5F6", edgecolor="black", alpha=0.8)

            # Add annotations for each bar
            for index, value in enumerate(values):
                plt.text(value + 0.5, index, str(value), va="center", fontsize=10)

            # Title and labels
            plt.title("Horizontal Bar Chart: Number of Students in Different Modules", fontsize=18, weight="bold")
            plt.xlabel("Number of Students", fontsize=14)
            plt.ylabel("Modules", fontsize=14)

            # Grid and styling
            plt.grid(axis="x", linestyle="--", alpha=0.7)
            plt.xticks(fontsize=12)
            plt.yticks(fontsize=12)

            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_pie_chart():
        data = read_csv()
        if not data: return

        gender_counts = {"Male": 0, "Female": 0}
        for row in data[1:]:
            gender_counts[row[7]] += 1

        plt.pie(gender_counts.values(), labels=gender_counts.keys(), autopct='%1.1f%%',
                startangle=140, colors=["#FF9999", "#66B2FF"])
        plt.title("Gender Distribution")
        plt.show()

    def show_grouped_bar_chart():
        data = read_csv()
        if not data: return

        header = data[0]
        rows = data[1:]

        coursework_columns = ["Coursework 1", "Coursework 2", "Coursework 3"]
        coursework_marks = {column: [] for column in coursework_columns}

        for row in rows:
            try:
                coursework_marks["Coursework 1"].append(int(row[4]))
                coursework_marks["Coursework 2"].append(int(row[5]))
                coursework_marks["Coursework 3"].append(int(row[6]))
            except (ValueError, IndexError):
                continue

        averages = {coursework: sum(marks) / len(marks) if marks else 0
                    for coursework, marks in coursework_marks.items()}

        plt.figure(figsize=(8, 6))
        plt.bar(averages.keys(), averages.values(), color=["#FF6347", "#4CAF50", "#2196F3"], alpha=0.8)

        plt.title("Average Marks for Coursework", fontsize=16)
        plt.xlabel("Coursework", fontsize=14)
        plt.ylabel("Average Marks", fontsize=14)
        plt.ylim(0, 100)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def show_date_of_entry_line_chart():
        data = read_csv()
        if not data: return

        date_counts = {}
        for row in data[1:]:
            date_counts[row[8]] = date_counts.get(row[8], 0) + 1

        sorted_dates = sorted(date_counts.items(), key=lambda x: x[0])
        dates, counts = zip(*sorted_dates)

        plt.figure(figsize=(10, 6))
        plt.plot(dates, counts, marker='o', color="#2196F3", linewidth=2)
        plt.title("Date of Entry Trend", fontsize=16)
        plt.xlabel("Date of Entry", fontsize=12)
        plt.ylabel("Number of Entries", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.show()

    def show_histogram_total_marks():
        data = read_csv()
        if not data: return

        try:
            total_marks = [
                (row[1], int(row[9]))
                for row in data[1:]
                if len(row) > 9 and row[9].isdigit()
            ]
        except (IndexError, ValueError):
            return messagebox.showinfo("Error", "Invalid or missing Total Marks column.")

        if not total_marks:
            return messagebox.showinfo("No Data", "No valid data available for total marks.")

        names, marks = zip(*total_marks)

        plt.figure(figsize=(12, 6))
        counts, bins, patches = plt.hist(marks, bins=10, edgecolor="black", alpha=0.75)
        plt.title("Distribution of Total Marks with Student Names")
        plt.xlabel("Total Marks")
        plt.ylabel("Frequency")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for name, mark in total_marks:
            for i in range(len(bins) - 1):
                if bins[i] <= mark < bins[i + 1]:
                    bin_center = (bins[i] + bins[i + 1]) / 2
                    bin_height = counts[i]
                    plt.text(bin_center, bin_height + 0.1, name, fontsize=8,
                             rotation=45, ha='center', va='bottom')
                    break

        plt.tight_layout()
        plt.show()
        
    tk.Button(frame, text="Show Module Bar Chart", command=show_horizontal_bar_chart, font=("Helvetica", 12), bg="#FFC107",
              fg="black").pack(pady=10)
    tk.Button(frame, text="Show Pie Chart", command=show_pie_chart, font=("Helvetica", 12), bg="#FF9800",
              fg="white").pack(pady=10)
    tk.Button(frame, text="Show Grouped Bar Chart", command=show_grouped_bar_chart, font=("Helvetica", 12),
              bg="#FFC107", fg="black").pack(pady=10)
    tk.Button(frame, text="Show Date of Entry Line Chart", command=show_date_of_entry_line_chart,
              font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(frame, text="Show Histogram for Total Marks", command=show_histogram_total_marks,
              font=("Helvetica", 12), bg="#FF5722", fg="white").pack(pady=10)
    
def stats_page():
    # Clear the current content of the frame
    clear_frame()

    # Display the Statistics page title
    tk.Label(frame, text="Statistics", font=("Helvetica", 16), bg="#B3E5FC").pack(pady=10)

    # Function to calculate and display statistics
    def calculate_stats():
        data = read_csv()[1:]  # Exclude the header row
        if not data:
            messagebox.showinfo("No Data", "No data available for statistics.")
            return

        total_marks = 0
        total_students = 0
        highest_marks = -1
        lowest_marks = 101

        for row in data:
            marks = [int(row[i]) for i in range(4, 7) if row[i].isdigit()]
            if marks:
                total_marks += sum(marks)
                total_students += 1
                highest_marks = max(highest_marks, max(marks))
                lowest_marks = min(lowest_marks, min(marks))

        if total_students == 0:
            messagebox.showinfo("No Data", "No valid coursework marks found.")
            return

        average_marks = total_marks / (total_students * 3)  # Assuming 3 coursework marks per student

        # Display the statistics on the UI
        stats_text = f"Total Marks: {total_marks}\n" \
                     f"Average Marks: {average_marks:.2f}\n" \
                     f"Highest Marks: {highest_marks}\n" \
                     f"Lowest Marks: {lowest_marks}"

        tk.Label(frame, text=stats_text, font=("Helvetica", 12), bg="#B3E5FC").pack(pady=10)

    # Add a button to calculate statistics
    tk.Button(
        frame,
        text="Calculate Stats",
        command=calculate_stats,
        font=("Helvetica", 12),
        bg="#FFC107",
        fg="black"
    ).pack(pady=10)


# Initialize the application
initialize_csv()

root = tk.Tk()
root.title("Mark Registration System")
root.geometry("800x600")
root.configure(bg="#B3E5FC")

tk.Label(root, text="Mark Registration System", font=("Helvetica", 34), bg="#64B5F6", fg="white").pack(fill="x", pady=5)

nav_bar = tk.Frame(root, bg="#B3E5FC")
nav_bar.pack(pady=10)

buttons = [
    ("Home", home_page),
    ("Input Mark", input_marks_page),
    ("Update Mark", update_marks_page),
    ("View Mark", view_marks_page),
    ("Visualization", visualize_page),
]

for text, command in buttons:
    tk.Button(nav_bar, text=text, command=command, font=("Helvetica", 12), bg="#4CAF50" if text == "Home" else
    ("#2196F3" if text == "Update Mark" else
     ("#FFC107" if text == "View Mark" else
      ("#9C27B0" if text == "Visualization" else "#F44336"))), fg="white" if text != "View Mark" else "black").pack(
        side="left", padx=10)

frame = tk.Frame(root, bg="#B3E5FC")
frame.pack(fill="both", expand=True)

if __name__ == '__main__':
    home_page()
    root.mainloop()
