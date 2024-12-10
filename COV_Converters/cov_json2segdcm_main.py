# -*- coding:utf-8 -*-
"""
Created on Fri. Oct. 25 13:49:34 2024
@author: JUN-SU PARK

JSON to DICOM Segmentation Conversion Main Script

This script orchestrates the conversion of JSON annotations to DICOM-SEG files by:
1. Processing patient directories
2. Converting JSON annotations to intermediate DICOM files
3. Creating final DICOM-SEG files from the intermediate files
"""
import os
import warnings
from tqdm import tqdm
from converters.json2segdicom_converters import convert_json_to_segdicom

# Suppress all warnings from pydicom
warnings.filterwarnings('ignore', category=UserWarning, module='pydicom')


def cov_segdcm_convert_process_all(base_dir: str) -> None:
    """
    Process all patient directories for JSON to DICOM-SEG conversion.

    This function scans a given base directory containing patient folders, identifies
    JSON annotation files within subdirectories, and performs the conversion into DICOM-SEG
    files using the `convert_json_to_segdicom` function.

    Args:
        base_dir (str): Path to the base directory containing patient folders.

    Returns:
        None: This function performs file modifications in-place within the directory.
    """
    # List all patient directories in the base directory
    patients_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    # Iterate through each patient directory
    for patient_dir in tqdm(patients_dirs, desc="Creating DICOM-SEG files", unit="patient"):
        # List all subdirectories (OR directories) for a given patient
        ord_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir) if os.path.isdir(os.path.join(patient_dir, f))]

        for ord_dir in ord_dirs:
            try:
                # Get the date directory within the OR directory
                date_ = os.listdir(ord_dir)[0]
                target_path = os.path.join(ord_dir, date_, 'TargetSequence')

                # Perform the JSON to DICOM-SEG conversion
                convert_json_to_segdicom(target_path)

            except Exception as e:
                # Print an error message if the conversion fails for a specific directory
                print(f"\nError processing patient '{os.path.basename(patient_dir)}', date '{date_}': {str(e)}")
                continue


if __name__ == '__main__':
    input_dir = r'C:\Users\BMC\Desktop\Dataset\TEST DATASET\Healthcare_CT\dataset\CT'
    cov_segdcm_convert_process_all(input_dir)
