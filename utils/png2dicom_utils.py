# -*- coding:utf-8 -*-
"""
Created on Thu. Aug. 29 17:20:13 2024
@author: JUN-SU Park
"""
import os
import pydicom
import numpy as np
from PIL import Image


def convert_png_to_dicom(png_file, dcm_ref_file, output_file):
    """
    Convert PNG array data to DICOM using a reference DICOM file.

    Args:
    png_file (str): Path to the JSON file containing annotation data.
    dcm_ref_file (str): Path to the reference DICOM file.
    output_file (str): Path to save the output DICOM file.
    """
    dcm_ref = pydicom.dcmread(dcm_ref_file)

    if os.path.exists(png_file):
        # Load PNG file if it exists
        png_img = Image.open(png_file).convert('L')
        mask_data = np.array(png_img)

        # Convert PNG values to DICOM range (0-255 -> -2000-2000)
        mask_data = mask_data / 50
        mask_data = mask_data.astype(np.int16)
    else:
        mask_data = np.full((dcm_ref.Rows, dcm_ref.Columns), 0, dtype=np.int16)

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