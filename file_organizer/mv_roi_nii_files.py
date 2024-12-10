# *coding:utf-8 -*

"""
Created on Fri. Nov. 29 10:16:21 2024
@author: JUN-SU PARK

Project Title: CT Dataset NII File Organizer

This module provides functionalities for:

1. Moving and renaming NII files from the dataset directories for better organization.
2. Handling segmentation NII files (if available) and saving them with appropriate names.
"""

import os
import shutil
from tqdm import tqdm


def move_and_rename_nii_files(base_dir: str, save_dir: str) -> None:
    """
    Moves and renames NII files and segmentation files from the dataset directories
    into a single output directory.

    Args:
        base_dir (str): Path to the base directory containing patient directories.
        save_dir (str): Path to the output directory where files will be saved.

    Returns:
        None: The function performs in-place modifications and saves files in the output directory.
    """
    os.makedirs(save_dir, exist_ok=True)

    # List all patient directories in the base directory
    patient_dirs = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    num = 1  # Counter for renaming files

    # Iterate through each patient directory with a progress bar
    for patient_dir in tqdm(patient_dirs, total=len(patient_dirs), desc='Move SEG NII files', unit='patient'):
        # Extract the patient name from the directory path
        patient_name = os.path.basename(patient_dir)

        # List all OR directories within the patient directory
        ord_dirs = [os.path.join(patient_dir, f) for f in os.listdir(patient_dir) if os.path.isdir(os.path.join(patient_dir, f))]
        seg_name = None
        label = None

        for ord_dir in ord_dirs:
            try:
                # Extract the date directory within the OR directory
                date_name = os.listdir(ord_dir)[0]
                target_path = os.path.join(ord_dir, date_name, "TargetSequence")

                # Path to the 'nii' directory and the first NII file
                nii_dir = os.path.join(target_path, 'nii')
                nii_path = os.path.join(nii_dir, os.listdir(nii_dir)[0])

                # Path to the segmentation directory (if exists)
                seg_dir = os.path.join(target_path, 'dcm_seg')
                try:
                    # Find the first segmentation file
                    seg_name = [f for f in os.listdir(seg_dir) if f.endswith('.nii.gz')][0]
                    seg_path = os.path.join(seg_dir, seg_name)
                    label = seg_name.split('_')[0]
                except IndexError:
                    # Skip if no segmentation file is found
                    seg_path = None
                    label = None
                    pass

                if seg_path is not None:
                    # Save NII file with a new name in the save directory
                    nii_save_path = os.path.join(save_dir, f'{str(num).zfill(3)}. [CT, {label}]_{patient_name}_{date_name}.nii.gz')
                    shutil.copyfile(nii_path, nii_save_path)
                    # Save segmentation file (if available) with a new name in the save directory
                    seg_save_path = os.path.join(save_dir, f'{str(num).zfill(3)}. [ROI, {label}]_{patient_name}_{date_name}.nii.gz')
                    shutil.copyfile(seg_path, seg_save_path)
                else:
                    nii_save_path = os.path.join(save_dir, f'{str(num).zfill(3)}. [CT, Normal]_{patient_name}_{date_name}.nii.gz')
                    shutil.copyfile(nii_path, nii_save_path)

                num += 1  # Increment the file counter
            except Exception as e:
                # Handle any exceptions during file handling
                print(f"Error processing {ord_dir}: {e}")
                pass


if __name__ == '__main__':
    base_dir = r'D:\DATASET\Healthcare\dataset\CT'
    save_dir = r'C:\Users\BMC\Desktop\Dataset\Healthcare_CT\dataset_roi'
    move_and_rename_nii_files(base_dir, save_dir)
