# -*- coding:utf-8 -*-
"""
Created on Mon. Aug. 05 10:32:11 2024
@author: JUN-SU Park
"""
import json
import pydicom
import numpy as np


def convert_json_to_dicom(json_file, dcm_ref_file, output_file):
    """
    Convert JSON array data to DICOM using a reference DICOM file.

    Args:
    json_file (str): Path to the JSON file containing annotation data.
    dcm_ref_file (str): Path to the reference DICOM file.
    output_file (str): Path to save the output DICOM file.
    """
    # Read JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Read reference DICOM file
    dcm_ref = pydicom.dcmread(dcm_ref_file)

    # Get image dimensions from the reference DICOM
    rows = dcm_ref.Rows
    columns = dcm_ref.Columns

    try:
        # Extract array data
        array_data = data['annotations']['mask'][0]['array']
        # Convert array data to numpy array and reshape
        mask_data = np.array([[int(pixel) for pixel in row] for row in array_data], dtype=np.uint16)
        mask_data[mask_data == 2] = 1

    # Handle empty array
    except IndexError:
        # Create an empty mask with the same dimensions as the reference image
        mask_data = np.zeros((rows, columns), dtype=np.uint16)

    # Create segmentation mask DICOM file
    dcm_seg = dcm_ref.copy()

    # Modify tags
    # dcm_seg.SeriesInstanceUID = uid_seed  # New Series UID
    dcm_seg.Modality = 'SEG'  # Change Modality || CT: 'CT', MRI: 'MRI', Segmentation: 'SEG'

    # Set Pixel Data and related attributes
    dcm_seg.PixelData = mask_data.tobytes()
    dcm_seg.SamplesPerPixel = 1  # Grayscale: 1, RGB: 3
    dcm_seg.PhotometricInterpretation = 'MONOCHROME2'  # Grayscale: 'MONOCHROME2', RGB: 'RGB'

    # Save the modified DICOM file
    dcm_seg.save_as(output_file)
