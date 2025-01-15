import os
import tkinter as tk
from tkinter import filedialog

def convert_to_trc(file_path):
    """
    Convert a CAN log file (.log or .txt) to a .trc format.
    
    :param file_path: Path to the input log file
    :return: Path to the saved .trc file
    """
    output_file = os.path.splitext(file_path)[0] + ".trc"

    try:
        with open(file_path, 'r') as infile, open(output_file, 'w') as outfile:
            # Write TRC header
            outfile.write(
                ";$FILEVERSION=1.3\n"  # Specify TRC version
                ";$STARTTIME=0\n"    # Placeholder start time
                ";$COLUMNS=N,Time,Type,ID,Length,Data\n"
                "\n"
            )

            for line in infile:
                parts = line.strip().split()
                if len(parts) < 3 or '#' not in parts[2]:
                    continue

                try:
                    timestamp = float(parts[0][1:-1])  # Strip parentheses and convert to float
                    can_id, data = parts[2].split('#')
                    length = len(data) // 2
                    
                    # Write the line in TRC format
                    outfile.write(
                        f"{int(timestamp * 1000)} ({timestamp:.3f}) Rx {can_id} - {length} {data}\n"
                    )
                except Exception as e:
                    print(f"Error processing line: {line}. Error: {e}")

        print(f"Conversion successful: {output_file}")
        return output_file

    except Exception as e:
        print(f"Failed to convert file. Error: {e}")
        return None

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root Tkinter window

    file_path = filedialog.askopenfilename(
        title="Select a CAN Log File",
        filetypes=[("Log and Text Files", "*.log;*.txt"), ("All Files", "*.*")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    trc_file = convert_to_trc(file_path)

    if trc_file:
        # Open the directory containing the .trc file in Windows Explorer
        os.startfile(os.path.dirname(trc_file))

if __name__ == "__main__":
    main()
