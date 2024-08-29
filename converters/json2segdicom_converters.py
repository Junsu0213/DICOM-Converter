# -*- coding:utf-8 -*-
"""
Created on Mon. Aug. 05 10:32:11 2024
@author: JUN-SU Park
"""
import os
import json
import shutil
import pydicom
from utils.json2dicom_utils import convert_json_to_dicom
from utils.create_seg_dcm_utils import create_seg_dicom


def move_annotations_to_original(annotation_dir):
    """Move existing annotation files to the 'original' subdirectory."""
    original_dir = os.path.join(annotation_dir, 'original')
    for file in os.listdir(annotation_dir):
        if file.endswith('.json') and os.path.isfile(os.path.join(annotation_dir, file)):
            shutil.move(os.path.join(annotation_dir, file), os.path.join(original_dir, file))
    print(f"Moved existing annotations to {original_dir}")


def convert_json_to_segdicom(input_dir, output_dir=None):
    """
    Process data for a single patient.

    Args:
    patient_dir (str): Directory containing patient data.
    seg_name (str): Name of the segmentation type (e.g., 'lobe', 'lesion').
    """

    print(f"Processing date: {input_dir}")
    annotation_dir = os.path.join(input_dir, 'annotation')
    dcm_dir = os.path.join(input_dir, 'dcm')
    temp_dcm_dir = os.path.join(input_dir, 'temp_dcm')

    # Create necessary directories
    for dir_name in ['annotation/original', 'annotation/Edit_ver1', 'temp_dcm']:
        os.makedirs(os.path.join(input_dir, dir_name), exist_ok=True)

    # Move existing annotations to 'original' subdirectory
    if os.path.exists(annotation_dir):
        move_annotations_to_original(annotation_dir)
    else:
        print(f"Warning: Annotation directory not found: {annotation_dir}")

    # Initialize variables
    label = None
    labels = set()
    temp_dcm_files = []
    initial_series_number = None

    # Convert JSON to DICOM
    original_dir = os.path.join(annotation_dir, 'original')
    json_files = sorted(os.listdir(original_dir))  # Ensure processing order
    series_num = 0
    # uid_seed = generate_uid()
    for json_file in json_files:
        if json_file.endswith('.json'):
            json_path = os.path.join(original_dir, json_file)
            dcm_ref_file = os.path.join(dcm_dir, json_file.replace('.json', '.dcm'))
            temp_dcm_file = os.path.join(temp_dcm_dir, json_file.replace('.json', '.dcm'))

            if os.path.exists(dcm_ref_file):
                # Read reference DICOM to check series number
                dcm_ref = pydicom.dcmread(dcm_ref_file)
                current_series_number = dcm_ref.SeriesNumber

                # If this is the first file, set the initial series number
                if initial_series_number is None:
                    initial_series_number = current_series_number

                # Check if series number has changed
                if current_series_number != initial_series_number:
                    print(f"Series number changed. Stopping processing")
                    break

                series_num += 1

                # Process the file if series number hasn't changed
                convert_json_to_dicom(json_path, dcm_ref_file, temp_dcm_file)
                temp_dcm_files.append(temp_dcm_file)

                # Extract label information
                with open(json_path, 'r') as f:
                    json_data = json.load(f)

                try:
                    label = json_data['annotations']['mask'][0]['disease']
                except IndexError:
                    pass

                if label is not None:  # Only add non-empty labels
                    labels.add(label)
                    label = None
            else:
                print(f"Warning: No corresponding DICOM file found for {json_file}")

    if not labels:
        # Clean up temporary DICOM files
        for file in temp_dcm_files:
            os.remove(file)
        os.rmdir(temp_dcm_dir)
    else:
        if temp_dcm_files:
            # Create SEG.DICOM
            create_seg_dicom(temp_dcm_dir, output_dir=output_dir, labels=labels)

            # Clean up temporary DICOM files
            for file in temp_dcm_files:
                os.remove(file)
            os.rmdir(temp_dcm_dir)
        else:
            print(f"No DICOM files were created for {input_dir}")


if __name__ == '__main__':
    input_dir = r'D:\DATASET\COVID_CT_Dataset\COV-CCO\COV-CCO-001\20210112'
    convert_json_to_segdicom(input_dir)