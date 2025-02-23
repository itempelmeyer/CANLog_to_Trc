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
                ";$FILEVERSION=2.1\n"
                ";$STARTTIME=45630.6373844296977\n"
                ";$COLUMNS=N,O,T,B,I,d,R,L,D\n"
                ";\n"
                ";   Start time: 12/4/2024 15:17:50.014.7\n"
                ";   Generated by PCAN-Explorer v6.7.0.2830\n"
                ";-------------------------------------------------------------------------------\n"
                ";   Bus  Connection   Net Connection           Protocol  Bit rate\n"
                ";   1    JCA Bus      JCA_250@pcan_usb         J1939     250 kbit/s\n"
                ";   2    Tractor BUS  JD_TractorCan@pcan_usb   J1939     500 kbit/s\n"
                ";   3    Virtual Bus  VirtualCAN@pcan_virtual  CAN       500 kbit/s\n"
                ";-------------------------------------------------------------------------------\n"
                ";   Message    Time    Type    ID     Rx/Tx\n"
                ";   Number     Offset  |  Bus  [hex]  |  Reserved\n"
                ";   |          [ms]    |  |    |      |  |  Data Length Code\n"
                ";   |          |       |  |    |      |  |  |    Data [hex] ...\n"
                ";   |          |       |  |    |      |  |  |    |\n"
                ";---+--- ------+------ +- +- --+----- +- +- +--- +- -- -- -- -- -- -- --\n"
            )

            message_number = 1
            first_timestamp = None

            for line in infile:
                parts = line.strip().split()
                if len(parts) < 8:  # Adjust to skip lines with too few fields
                    continue

                try:
                    # Extract timestamp and calculate relative offset
                    timestamp = float(parts[0][1:-1])  # Strip parentheses and convert to float
                    if first_timestamp is None:
                        first_timestamp = timestamp
                    relative_time = (timestamp - first_timestamp) * 1000

                    # Extract bus, ID, and data
                    bus = parts[1]
                    can_id = parts[5]
                    data_length = int(parts[6][1:-1])  # Strip brackets and convert to int
                    data = " ".join(parts[7:7 + data_length])

                    # Write the formatted line to the output file
                    outfile.write(
                        f"{str(message_number).rjust(8)}      {relative_time:8.3f} DT {bus[-1]}  {can_id} Rx -  {data_length:<4} {data}\n"
                    )
                    message_number += 1
                except Exception as e:
                    print(f"Error processing line: {line.strip()} -> {e}")

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
