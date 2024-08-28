# -*- coding:utf-8 -*-
"""
Created on Sat. Aug. 10 18:01:08 2024
@author: JUN-SU Park
"""
import nii2png
import os
from concurrent.futures import ThreadPoolExecutor
import logging

# Define constants
DATA_DIR = '/mnt/nasw337n2/junsu_work/DATASET/MRI'
NII_DIR = os.path.join(DATA_DIR, 'CEData')
PNG_DIR = os.path.join(DATA_DIR, 'CEData_png')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def convert_nii_to_png(input_file, output_dir=None):
    # If output_dir is not provided, create a new directory
    if output_dir is None:
        # Get the directory of the input file
        input_dir = os.path.dirname(input_file)
        # Go up one level
        parent_dir = os.path.dirname(input_dir)
        # Create a new 'png' directory next to the 'nii' directory
        output_dir = os.path.join(parent_dir, 'png')

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Convert NII to PNG using nii to png function
        nii2png.convert_nii_to_png(input_file, output_dir)
        logging.info(f"Converted {output_dir} to PNG")
    except Exception as e:
        logging.error(f"Error converting {input_file}: {str(e)}")


def process_patient(folder_name):
    # Construct file paths
    file_name = f'{folder_name}/{folder_name}_predictions_breast_simulated_gad.nii.gz'
    patient_nii_file = os.path.join(NII_DIR, file_name)
    patient_png_dir = os.path.join(PNG_DIR, folder_name)

    # Check if the NII file exists
    if not os.path.exists(patient_nii_file):
        logging.warning(f"File not found: {patient_nii_file}")
        return

    # Create patient-specific output directory
    os.makedirs(patient_png_dir, exist_ok=True)

    # Convert NII to PNG
    convert_nii_to_png(patient_nii_file, patient_png_dir)


def main():
    """Main function to process all patients."""
    # Check if the NII directory exists
    if not os.path.exists(NII_DIR):
        logging.error(f"NII directory not found: {NII_DIR}")
        return

    # Get list of all patient folders
    folder_names = os.listdir(NII_DIR)
    logging.info(f"Found {len(folder_names)} folders to process")

    # Process patients in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        list(executor.map(process_patient, folder_names))

    logging.info("Processing complete")


if __name__ == '__main__':
    main()
