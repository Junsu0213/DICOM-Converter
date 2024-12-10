# *coding:utf-8 -*

"""
Created on Fri. Nov. 29 10:14:11 2024
@author: JUN-SU PARK

Project Title: CT Dataset Sequence Organizer

This module provides functionalities for:

1. Identifying the sequence with the most files in each directory.
2. Renaming directories to the target sequence for easier access and consistency.
"""

import os


def organize_ct_sequences(base_dir: str) -> None:
    """
    Organizes CT dataset directories by identifying and renaming
    directories with the most files in each sequence.

    Args:
        base_dir (str): Path to the base directory containing patient directories.

    Returns:
        None: The function performs in-place modifications to the directory structure.
    """
    # List all patient directories in the base directory
    patient_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for patient_dir in patient_dirs:
        # List all OR directories for a given patient
        or_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir) if os.path.isdir(os.path.join(patient_dir, f))]

        for or_dir in or_dirs:
            try:
                # Assume the first item in the OR directory is the date folder
                date_name = os.listdir(or_dir)[0]
                date_dirs = [os.path.join(or_dir, date_name) for _ in os.listdir(or_dir)]

                for date_dir in date_dirs:
                    # Retrieve the list of sequences in the date directory
                    seq_list = os.listdir(date_dir)

                    max_seq_name = None
                    max_file_count = 0

                    for seq in seq_list:
                        try:
                            # Path to the 'dcm' directory of the current sequence
                            dcm_dir = os.path.join(date_dir, seq, 'dcm')
                            file_count = len(os.listdir(dcm_dir))

                            # Update if the current sequence has more files
                            if file_count > max_file_count:
                                max_file_count = file_count
                                max_seq_name = seq
                        except Exception:
                            # Skip if there's an error in accessing the sequence directory
                            pass

                    # Rename the directory to the sequence with the most files
                    if max_seq_name is not None:
                        new_name = os.path.join(date_dir, "TargetSequence")
                        current_seq_dir = os.path.join(date_dir, max_seq_name)

                        # Check if the new name already exists to avoid conflicts
                        if not os.path.exists(new_name):
                            os.rename(current_seq_dir, new_name)
                            print(f"Renamed {current_seq_dir} to {new_name}")
                        else:
                            print(f"Skipped renaming {current_seq_dir}, {new_name} already exists.")
            except Exception:
                # Skip if there's an error in processing the OR directory
                pass


if __name__ == "__main__":
    base_dir = r'D:\DATASET\Healthcare\dataset\CT'
    organize_ct_sequences(base_dir)