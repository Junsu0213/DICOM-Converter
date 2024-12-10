# *coding:utf-8 -*

"""
Created on Wed. Nov. 27 14:11:22 2024
@author: JUN-SU PARK

DICOM and Related Files Organizer

This module provides functionalities for:

1. Adding ordinal directories (1st, 2nd, etc.) to date folders.
2. Organizing DICOM files and related files (annotation, png, etc.) into Series Description folders.
3. Special handling for 'COV-SCO' files, including removal of specific files.
"""

import os
import shutil
import pydicom
from tqdm import tqdm


def add_ordinal_directories(base_dir: str) -> None:
    """
    Adds ordinal directories (1st, 2nd, etc.) to date folders under patient directories.
    Skips patient directories that are already processed.

    Args:
        base_dir (str): The base directory containing patient directories.

    Returns:
        None
    """
    # Traverse patient directories
    patient_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for patient_dir in tqdm(patient_dirs, desc="Adding Ordinal Directories", unit="patient"):
        # Get date folders within the patient directory
        date_list = [d for d in os.listdir(patient_dir) if os.path.isdir(os.path.join(patient_dir, d))]

        # Skip directories that already have ordinal folders (e.g., '1st', '2nd')
        if any(name.endswith(('st', 'nd', 'rd', 'th')) for name in date_list):
            continue

        # Sort the date folders to ensure consistent ordinal naming
        date_list.sort()

        # Convert numbers to ordinal strings (e.g., 1 -> '1st', 2 -> '2nd')
        def ordinal(n: int) -> str:
            """
            Converts a number to an ordinal string.

            Args:
                n (int): The number to convert.

            Returns:
                str: The ordinal representation of the number.
            """
            suffix = ['st', 'nd', 'rd'] + ['th'] * 7
            if 10 <= n % 100 <= 20:
                return f"{n}th"
            else:
                return f"{n}{suffix[(n % 10) - 1]}"

        # Create ordinal folders and move corresponding date folders into them
        for idx, date in enumerate(date_list, start=1):
            new_dir_name = ordinal(idx)  # e.g., '1st', '2nd'
            new_dir_path = os.path.join(patient_dir, new_dir_name)

            # Create the ordinal directory if it does not exist
            if not os.path.exists(new_dir_path):
                os.mkdir(new_dir_path)

            # Move the date folder into the newly created ordinal directory
            old_date_path = os.path.join(patient_dir, date)
            new_date_path = os.path.join(new_dir_path, date)
            shutil.move(old_date_path, new_date_path)


def organize_dicom_by_series(base_dir: str) -> None:
    """
    Organizes DICOM files and related files into Series Description folders.
    Handles special cases for specific SeriesDescriptions and removes redundant files.

    Args:
        base_dir (str): The base directory containing organized patient directories.

    Returns:
        None
    """
    # Traverse patient directories and their subdirectories
    for root, dirs, files in tqdm(os.walk(base_dir), desc="Organizing DICOM Files", unit="directory"):
        # Skip non-target directories
        if not any(sub in root for sub in ["annotation", "dcm", "png", "png_lesion", "png_lobe", "nii"]):
            continue

        # Remove 'nii' directories as they are not needed
        if "nii" in root:
            shutil.rmtree(root)
            continue

        # Process DICOM files located in 'dcm' directories
        if "dcm" in root:
            date_dir = os.path.dirname(root)  # The parent directory containing the date folders
            dcm_files = [f for f in files if f.endswith(".dcm")]

            # Sort DICOM files to ensure consistent ordering for special handling
            dcm_files.sort()

            for idx, dcm_file in enumerate(dcm_files):
                dcm_path = os.path.join(root, dcm_file)
                try:
                    # Load DICOM metadata to extract Series Description
                    ds = pydicom.read_file(dcm_path)
                except Exception as e:
                    # Skip unreadable DICOM files
                    continue

                # Get the Series Description or use 'Unknown' if not available
                series_description = getattr(ds, "SeriesDescription", "Unknown")

                # Special case: For 'COV-SCO' and 'Lung 3mm AXL', remove the first two files
                if "COV-SCO" in root and series_description == "Lung 3mm AXL" and idx < 2:
                    os.remove(dcm_path)
                    continue

                # Create a folder for the Series Description if it does not exist
                series_dir = os.path.join(date_dir, series_description)
                os.makedirs(series_dir, exist_ok=True)

                # Move the DICOM file into the corresponding Series Description folder
                series_dcm_dir = os.path.join(series_dir, "dcm")
                os.makedirs(series_dcm_dir, exist_ok=True)
                shutil.move(dcm_path, os.path.join(series_dcm_dir, dcm_file))

                # Process related files (e.g., annotation, png, etc.)
                for sub_dir in ["annotation", "png", "png_lesion", "png_lobe"]:
                    related_dir = os.path.join(date_dir, sub_dir)
                    if not os.path.exists(related_dir):
                        continue

                    # Check for annotation files and move them
                    related_annotation_file = os.path.join(related_dir, dcm_file.replace(".dcm", ".json"))
                    if os.path.exists(related_annotation_file):
                        series_sub_dir = os.path.join(series_dir, sub_dir)
                        os.makedirs(series_sub_dir, exist_ok=True)
                        shutil.move(related_annotation_file, os.path.join(series_sub_dir, os.path.basename(related_annotation_file)))

                    # Check for image files and move them
                    related_image_file = os.path.join(related_dir, dcm_file.replace(".dcm", ".png"))
                    if os.path.exists(related_image_file):
                        series_sub_dir = os.path.join(series_dir, sub_dir)
                        os.makedirs(series_sub_dir, exist_ok=True)
                        shutil.move(related_image_file, os.path.join(series_sub_dir, os.path.basename(related_image_file)))

            # Remove original directories after all files are processed
            for sub_dir in ["dcm", "annotation", "png", "png_lesion", "png_lobe"]:
                dir_to_remove = os.path.join(date_dir, sub_dir)
                if os.path.exists(dir_to_remove):
                    shutil.rmtree(dir_to_remove)


if __name__ == "__main__":
    data_list = ['COV-CCO', 'COV-SCO']
    for data in data_list:
        # Example usage
        base_directory = rf"D:\DATASET\Healthcare\1차\dataset\{data}"
        add_ordinal_directories(base_directory)  # Step 1: Add ordinal directories
        organize_dicom_by_series(base_directory)  # Step 2: Organize files by Series Description
