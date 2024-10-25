# -*- coding:utf-8 -*-
"""
Created on Mon. Aug. 05 10:32:11 2024
@author: JUN-SU Park

JSON to DICOM Segmentation Conversion Module

This module provides functionality to:
1. Convert JSON annotations to DICOM format
2. Create DICOM-SEG files from annotations
3. Handle file organization and cleanup
"""
import os
import json
import shutil
import warnings
import pydicom
from utils.json2dicom_utils import convert_json_to_dicom
from utils.create_seg_dcm_utils import create_seg_dicom

# Suppress all warnings from pydicom
warnings.filterwarnings('ignore', category=UserWarning, module='pydicom')


def move_annotations_to_original(annotation_dir: str) -> None:
    """
    Move existing annotation files to the 'original' subdirectory.

    Args:
        annotation_dir: Directory containing annotation files
    """
    original_dir = os.path.join(annotation_dir, 'original')
    for file in os.listdir(annotation_dir):
        if file.endswith('.json') and os.path.isfile(os.path.join(annotation_dir, file)):
            shutil.move(os.path.join(annotation_dir, file), os.path.join(original_dir, file))
    # print(f"Moved existing annotations to {original_dir}")


def convert_json_to_segdicom(input_dir: str, output_dir: str = None) -> None:
    """
    Convert JSON annotations to DICOM-SEG format for a single date directory.

    Args:
        input_dir: Directory containing patient data for a specific date
        output_dir: Optional output directory for converted files
    """
    # print(f"Processing date: {input_dir}")

    # Define directory paths
    annotation_dir = os.path.join(input_dir, 'annotation')
    dcm_dir = os.path.join(input_dir, 'dcm')
    temp_dcm_dir = os.path.join(input_dir, 'temp_dcm')

    # Create necessary directories
    for dir_name in ['annotation/original', 'annotation/Edit_ver1', 'temp_dcm']:
        os.makedirs(os.path.join(input_dir, dir_name), exist_ok=True)

    # Handle existing annotations
    if os.path.exists(annotation_dir):
        move_annotations_to_original(annotation_dir)
    else:
        print(f"Warning: Annotation directory not found: {annotation_dir}")

    # Initialize processing variables
    label = None
    labels = set()
    temp_dcm_files = []
    initial_series_number = None

    # Process JSON files
    original_dir = os.path.join(annotation_dir, 'original')
    json_files = sorted(os.listdir(original_dir))
    series_num = 0

    for json_file in json_files:
        if not json_file.endswith('.json'):
            continue

        json_path = os.path.join(original_dir, json_file)
        dcm_ref_file = os.path.join(dcm_dir, json_file.replace('.json', '.dcm'))
        temp_dcm_file = os.path.join(temp_dcm_dir, json_file.replace('.json', '.dcm'))

        if not os.path.exists(dcm_ref_file):
            print(f"Warning: No corresponding DICOM file found for {json_file}")
            continue

        # Check series consistency
        dcm_ref = pydicom.dcmread(dcm_ref_file)
        current_series_number = dcm_ref.SeriesNumber

        if initial_series_number is None:
            initial_series_number = current_series_number
        elif current_series_number != initial_series_number:
            # print(f"Series number changed. Stopping processing")
            break

        series_num += 1

        # Convert JSON to intermediate DICOM
        convert_json_to_dicom(json_path, dcm_ref_file, temp_dcm_file)
        temp_dcm_files.append(temp_dcm_file)

        # Extract label information
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        try:
            label = json_data['annotations']['mask'][0]['disease']
            if label:  # Only add non-empty labels
                labels.add(label)
        except (IndexError, KeyError):
            pass

    # Handle results and cleanup
    if not labels:
        # Clean up if no valid labels found
        for file in temp_dcm_files:
            os.remove(file)
        os.rmdir(temp_dcm_dir)
    else:
        if temp_dcm_files:
            # Create final DICOM-SEG file
            create_seg_dicom(temp_dcm_dir, output_dir=output_dir, labels=labels)

            # Cleanup temporary files
            for file in temp_dcm_files:
                os.remove(file)
            os.rmdir(temp_dcm_dir)
        else:
            print(f"No DICOM files were created for {input_dir}")


if __name__ == '__main__':
    input_dir = r'D:\DATASET\COVID_CT_Dataset\COV-CCO\COV-CCO-001\20210112'
    convert_json_to_segdicom(input_dir)