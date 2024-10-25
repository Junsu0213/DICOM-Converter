# -*- coding:utf-8 -*-
"""
Created on Fri. Oct. 25 13:17:22 2024
@author: JUN-SU PARK

This script orchestrates the DICOM metadata conversion process by:
1. Traversing through patient directories
2. Extracting clinical information from JSON annotations
3. Updating DICOM metadata with the extracted information
"""
import os
import warnings
from tqdm import tqdm
from converters.dicom_metainfo_converters import (
    extract_label_form_json,
    convert_dicom_metainfo
)
# Suppress specific pydicom warnings
warnings.filterwarnings('ignore', category=UserWarning, module='pydicom')


def cco_metainfo_convert_process_all(input_dir: str) -> None:
    """
    Process all patient directories and update DICOM metadata.
    Shows progress with tqdm progress bar.

    Args:
        input_dir: Base directory containing patient folders

    Directory structure expected:
    input_dir/
    ├── patient_id/
    │   ├── date/
    │   │   ├── annotation/
    │   │   │   └── original/
    │   │   │       └── annotation files
    │   │   └── dcm/
    │   │       └── DICOM files
    """
    # Get list of all patients
    patients = os.listdir(input_dir)

    # Create progress bar
    for patient_id in tqdm(patients, desc="Updating DICOM MetaInfo", unit="patient"):
        patient_path = os.path.join(input_dir, patient_id)

        # Process each date directory for the patient
        date_dirs = os.listdir(patient_path)
        for date_dir in date_dirs:
            date_path = os.path.join(patient_path, date_dir)

            # Define paths for JSON annotations and DICOM files
            json_dir = os.path.join(date_path, 'annotation', 'original')
            dcm_dir = os.path.join(date_path, 'dcm')

            try:
                # Extract information and update DICOM metadata
                label, sex = extract_label_form_json(json_dir)
                convert_dicom_metainfo(dcm_dir, label, sex)
            except Exception as e:
                print(f"\nError processing {patient_id} - {date_dir}: {str(e)}")
                continue


if __name__ == '__main__':
    # Example usage
    input_dir = r'C:\Users\BMC\Desktop\COV-CCO-test'
    cco_metainfo_convert_process_all(input_dir)
