# -*- coding:utf-8 -*-
"""
Created on Thu. Aug. 29 17:19:21 2024
@author: JUN-SU Park
"""
import os
import json
import shutil
import pydicom
from utils.png2dicom_utils import convert_png_to_dicom
from utils.create_seg_dcm_utils import create_seg_dicom


def convert_png_to_segdicom(input_dir, output_dir=None):
    """
    Process data for a single patient.

    Args:
    patient_dir (str): Directory containing patient data.
    seg_name (str): Name of the segmentation type (e.g., 'lobe', 'lesion').
    """
    dcm_dir = os.path.join(input_dir, 'dcm')
    temp_dcm_dir = os.path.join(input_dir, 'temp_dcm')

    os.makedirs(temp_dcm_dir, exist_ok=True)

