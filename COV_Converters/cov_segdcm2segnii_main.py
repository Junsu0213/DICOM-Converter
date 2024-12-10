# *coding:utf-8 -*

"""
Created on Thu. 28. Nov. 13:25:22 2024
@author: JUN-SU PARK

DICOM to NIfTI Conversion

This module provides functionalities for:

1. Converting DICOM-SEG files into NIfTI-SEG format.
2. Batch processing all patient directories and handling errors gracefully during conversion.

"""

import os
import warnings
from tqdm import tqdm
from converters.segdicom2segnii_converters import convert_segdcm_to_segnii

# Suppress unnecessary warnings to keep output clean
warnings.filterwarnings("ignore")


def cov_segdcm_to_segnii_preocess_all(base_dir: str) -> None:
    """
    Batch process all DICOM-SEG files in the given directory and convert them into NIfTI-SEG format.

    Args:
        base_dir (str): Path to the base directory containing patient subdirectories.

    Returns:
        None: This function does not return anything but processes files and saves results directly.
    """
    # Retrieve all patient directories in the specified base directory
    patient_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir)]

    # Iterate through each patient directory
    for patient_dir in tqdm(patient_dirs, total=len(patient_dirs), desc='Convert DICOM-SEG to NII-SEG files',
                            unit='patient'):

        # Retrieve subdirectories within the patient directory
        ord_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir)]

        for ord_dir in ord_dirs:
            # Construct the path to the target DICOM-SEG directory
            date_name = os.listdir(ord_dir)[0]
            target_path = os.path.join(ord_dir, date_name, 'TargetSequence', 'dcm_seg')

            try:
                # Convert the DICOM-SEG files into NIfTI-SEG format
                convert_segdcm_to_segnii(target_path)
            except Exception:
                # Ignore any errors during conversion
                pass


if __name__ == '__main__':
    base_dir = r'C:\Users\BMC\Desktop\Dataset\TEST DATASET\Healthcare_CT\dataset\CT'
    cov_segdcm_to_segnii_preocess_all(base_dir)