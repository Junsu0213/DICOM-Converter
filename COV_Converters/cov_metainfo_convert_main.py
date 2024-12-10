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


def cov_metainfo_convert_process_all(base_dir: str) -> None:
    """
    Process all patient directories and update DICOM metadata.
    Shows progress with tqdm progress bar.

    Args:
        base_dir: Base directory containing patient folders

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
    patient_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir)]

    # Create progress bar
    for patient_dir in tqdm(patient_dirs, desc="Updating DICOM MetaInfo", unit="patient"):

        # Process each date directory for the patient
        ord_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir)]

        for ord_dir in ord_dirs:
            date_ = os.listdir(ord_dir)[0]
            target_path = os.path.join(ord_dir, date_, 'TargetSequence')

            # Define paths for JSON annotations and DICOM files
            json_dir = os.path.join(target_path, 'annotation', 'original')
            dcm_dir = os.path.join(target_path, 'dcm')

            try:
                # Extract information and update DICOM metadata
                label, sex = extract_label_form_json(json_dir)
                convert_dicom_metainfo(dcm_dir, label, sex)
            except Exception as e:
                print(f"\nError processing {patient_dir.split('\\')[-1]} - {date_}: {str(e)}")
                continue


if __name__ == '__main__':
    # Example usage
    input_dir = r'C:\Users\BMC\Desktop\Dataset\TEST DATASET\Healthcare_CT\dataset\CT'
    cov_metainfo_convert_process_all(input_dir)