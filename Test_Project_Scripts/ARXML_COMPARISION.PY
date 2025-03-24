import difflib

import re

import tkinter as tk

from tkinter import filedialog
import os

def select_file(title):

    """Open a file dialog to select a file."""

    root = tk.Tk()

    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(title=title, filetypes=[("ARXML Files", "*.arxml"), ("All Files", "*.*")])

    return file_path

def remove_uuid(line):

    """Remove UUID attributes from an ARXML line."""

    return re.sub(r'uuid="[^"]+"', '', line, flags=re.IGNORECASE)

def compare_arxml_files(file1, file2, output_txt):

    """Compare two ARXML files and generate a text report with separators, ignoring UUID changes."""

    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:

        lines1 = f1.readlines()

        lines2 = f2.readlines()

    # Remove UUIDs before comparison

    lines1_clean = [remove_uuid(line).strip() for line in lines1]

    lines2_clean = [remove_uuid(line).strip() for line in lines2]

    diff = difflib.ndiff(lines1_clean, lines2_clean)

    changes = []

    line_num1 = 0  # Track line numbers in file1

    line_num2 = 0  # Track line numbers in file2

    for line in diff:

        if line.startswith("  "):  # No change

            line_num1 += 1

            line_num2 += 1

        elif line.startswith("- "):  # Line removed or changed

            line_num1 += 1

            original_line = line[2:].strip()

            if original_line == "":  

                continue  # Ignore empty lines

            changes.append(f"Line {line_num1} (Old File): {original_line}")

        elif line.startswith("+ "):  # Line added or changed

            line_num2 += 1

            added_line = line[2:].strip()

            if added_line == "":  

                continue  # Ignore empty lines

            changes.append(f"Line {line_num2} (New File): {added_line}")

            changes.append("-------------------------")  # Separator

    # Filter out UUID-only changes

    filtered_changes = []

    i = 0

    while i < len(changes) - 1:

        if "(Old File)" in changes[i] and "(New File)" in changes[i + 1]:

            old_line = changes[i].split(": ", 1)[1]

            new_line = changes[i + 1].split(": ", 1)[1]

            if remove_uuid(old_line) == remove_uuid(new_line):

                i += 2  # Skip this UUID-only change

                continue

        filtered_changes.append(changes[i])

        i += 1

    # Save to TXT file

    with open(output_txt, "w", encoding="utf-8") as txt_file:

        txt_file.write("\n".join(filtered_changes))

    print(f"Comparison completed. Changes saved to {output_txt}")

if __name__ == "__main__":

    default_arxml_file = r"C:\Users\hss930284\Tata Technologies\MBSE Team - SAARCONN - SAARCONN\Eliminating_SystemDesk\tests\Harshit_arelements_validation_24_03\COMBINED_AUTOMATION\Default_Files\Default_Input_arxml.arxml"


    import os

    from excel_utils import Excelfile_name

    print("The latest Excel file name is:", Excelfile_name)

    # Define the directory for ARXML files

    Arxml_directory = r"C:\Users\hss930284\Tata Technologies\MBSE Team - SAARCONN - SAARCONN\Eliminating_SystemDesk\tests\Harshit_arelements_validation_24_03\COMBINED_AUTOMATION\Intermidiate_Outputs\Generated_ARXML"

    # Ensure the directory exists

    os.makedirs(Arxml_directory, exist_ok=True)

    # Generate ARXML file path

    arxml_file_path = os.path.join(Arxml_directory, f"{Excelfile_name}.arxml")

    generated_arxml_file = arxml_file_path

    # Define output text file name using Excel file name

    Arxml_compared_txt_file = r"C:\Users\hss930284\Tata Technologies\MBSE Team - SAARCONN - SAARCONN\Eliminating_SystemDesk\tests\Harshit_arelements_validation_24_03\COMBINED_AUTOMATION\Comparator_Reports\ARXML_Comparator"

    os.makedirs(Arxml_compared_txt_file, exist_ok=True)  # Ensure output directory exists

    output_txt = os.path.join(Arxml_compared_txt_file, f"{Excelfile_name}.txt")  # Save log file using Excel name

    # Ensure both ARXML files exist before comparison

    if default_arxml_file and generated_arxml_file:

        compare_arxml_files(default_arxml_file, generated_arxml_file, output_txt)

    print(f"Comparison log saved to: {output_txt}") 