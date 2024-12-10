# *coding:utf-8 -*

"""
Created on Wed. Nov. 27 14:43:41 2024
@author: JUN-SU PARK

[Convert DICOM to NIfTI]

This module provides functionalities for:

1. Removing existing NIfTI directories before conversion.
2. Converting DICOM files to NIfTI format for each patient and sequence.
"""

import os
import shutil
from tqdm import tqdm
from converters.dicom2nii_converters import convert_dicom_to_nii


def remove_and_convert_dicom_to_nii(base_dir: str) -> None:
    """
    Removes existing NIfTI directories and converts DICOM files to NIfTI format.

    Args:
        base_dir (str): The base directory containing patient subdirectories.

    Returns:
        None
    """
    # List all patient directories within the base directory
    patient_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for patient_dir in tqdm(patient_dirs, desc="Convert dcm to nii file", unit="patient"):
        or_dirs = [os.path.join(patient_dir, d) for d in os.listdir(patient_dir)]

        for or_dir in or_dirs:
            date_name = os.listdir(or_dir)[0]
            date_dir = os.path.join(or_dir, date_name)
            seq_list = os.listdir(date_dir)

            for seq_dir in seq_list:
                input_dir = os.path.join(date_dir, seq_dir, 'dcm')
                nii_dir = os.path.join(date_dir, seq_dir, 'nii')

                # Remove existing NIfTI directory if it exists
                if os.path.exists(nii_dir):
                    shutil.rmtree(nii_dir)

                # Convert DICOM to NIfTI
                convert_dicom_to_nii(input_dir, file_name=seq_dir)


if __name__ == '__main__':
    base_dir = rf'D:\DATASET\Healthcare\dataset\CT_'
    remove_and_convert_dicom_to_nii(base_dir)
