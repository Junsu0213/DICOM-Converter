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


def cco_segdcm_convert_process_all(input_dir: str) -> None:
    """
    Process all patients' data for JSON to DICOM-SEG conversion.

    Args:
        input_dir: Base directory containing patient folders
    """
    # Get list of all patients
    patients = os.listdir(input_dir)

    # Process each patient with progress tracking
    for patient_id in tqdm(patients, desc="Creating DICOM-SEG files", unit="patient"):
        patient_path = os.path.join(input_dir, patient_id)

        # Process each date directory for the patient
        date_dirs = os.listdir(patient_path)
        for date_dir in date_dirs:
            date_path = os.path.join(patient_path, date_dir)
            convert_json_to_segdicom(date_path)


if __name__ == '__main__':
    input_dir = r'C:\Users\BMC\Desktop\COV-CCO-test'
    cco_segdcm_convert_process_all(input_dir)
