import difflib
import re
import pandas as pd
import os
import os
from excel_utils import Excelfile_name

def remove_uuid(line):
   """Remove UUID attributes from an ARXML line."""
   return re.sub(r'uuid="[^"]+"', '', line, flags=re.IGNORECASE)
def get_text_difference(old_text, new_text):
   """Extract and highlight only the changed words inside XML attributes."""
   # Tokenize XML content properly
   old_words = re.split(r'(\W+)', old_text)  # Keeps XML tags and separators
   new_words = re.split(r'(\W+)', new_text)
   # Compute difference
   diff = list(difflib.ndiff(old_words, new_words))
   removed_words = [word[2:] for word in diff if word.startswith("- ")]
   added_words = [word[2:] for word in diff if word.startswith("+ ")]
   # Format output
   if removed_words and added_words:
       return f"Changed: {' '.join(removed_words)} → {' '.join(added_words)}"
   elif removed_words:
       return f"Removed: {' '.join(removed_words)}"
   elif added_words:
       return f"Added: {' '.join(added_words)}"
   return "No Significant Change"
def compare_arxml_files(file1, file2, output_excel):
   """Compare two ARXML files and generate an Excel report with detailed changes."""
   with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
       lines1 = f1.readlines()
       lines2 = f2.readlines()
   # Remove UUIDs before comparison
   lines1_clean = [remove_uuid(line).strip() for line in lines1]
   lines2_clean = [remove_uuid(line).strip() for line in lines2]
   diff = list(difflib.ndiff(lines1_clean, lines2_clean))
   changes = []
   line_num1 = 0  
   line_num2 = 0  
   prev_original = None  
   for line in diff:
       if line.startswith(" "):  
           line_num1 += 1
           line_num2 += 1
           prev_original = line[2:].strip()
       elif line.startswith("- "):  
           line_num1 += 1
           prev_original = line[2:].strip()
       elif line.startswith("+ "):  
           line_num2 += 1
           added_line = line[2:].strip()
           if prev_original:
               difference = get_text_difference(prev_original, added_line)
               changes.append([line_num1, line_num2, "Modified", prev_original, added_line, difference])
           else:
               changes.append([None, line_num2, "Added", None, added_line, "New Line Added"])
           prev_original = None  
   
   df = pd.DataFrame(changes, columns=["Old Line No", "New Line No", "Change Type", "Original Content", "Updated Content", "Difference Highlight"])
   df.to_excel(output_excel, index=False)
   print(f"Comparison completed. Changes saved to {output_excel}")
  
   
if __name__ == "__main__":
   
    print("The latest Excel file name is:", Excelfile_name)
    Arxml_directory = r"C:\Users\sss923875\OneDrive - Tata Technologies\SAARCONN\Eliminating_SystemDesk\tests\Saurabh_validation_21_02\COMBINED_AUTOMATION\Intermidiate_Outputs\Generated_ARXML"
    os.makedirs(Arxml_directory, exist_ok=True)
    arxml_file_path = os.path.join(Arxml_directory, f"{Excelfile_name}.arxml")
    file1 =  r"C:\Users\sss923875\OneDrive - Tata Technologies\SAARCONN\Eliminating_SystemDesk\tests\Saurabh_validation_21_02\COMBINED_AUTOMATION\Default_Files\Default_Input_arxml.arxml"  
    file2 =  arxml_file_path    
    Arxml_compared_txt_file = r"C:\Users\sss923875\OneDrive - Tata Technologies\SAARCONN\Eliminating_SystemDesk\tests\Saurabh_validation_21_02\COMBINED_AUTOMATION\Comparator_Reports\ARXML_Comparator"
    os.makedirs(Arxml_compared_txt_file, exist_ok=True) 
    output_excel = os.path.join(Arxml_compared_txt_file, f"{Excelfile_name}.xlsx")  
      

    compare_arxml_files(file1, file2, output_excel) 
    
    
